from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import View, ListView, CreateView
from .forms import updateLoanForm, LoanApplicationForm, DocumentsForm, newLoanForm, ProposalForm
from loan_management.models import loanAmortization, LoanApplication, Loan, Document, ProposedApplication
from loan_management.logic import LoanCalculations
import csv
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from  authentication.models import Customer, BankAccount, Occupation

class CreateLoanTest(CreateView):
    template_name = 'admin-dashboard/admin-create-loan.html'
    form_class = newLoanForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class AdminViewLoans(ListView):
    model = Loan
    template_name = 'admin-dashboard/Add-loan.html'

def ProposalView(request):
    data = dict()
    if request.POST:
        form = ProposalForm(request.POST)
        loan_application_id = request.POST.get('loan_id')
        loanapplication =LoanApplication.objects.get(loanApp_id = loan_application_id)

        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.loanapplication = loanapplication
            proposal.user = loanapplication.user
            proposal.save()
            loanapplication.declined_and_propose = True
            loanapplication.isClosed=True
            loanapplication.save()
            messages.success(request, f'Proposal has been sent to the borrower')
            message = 'Good day! I would like to inform you that your loan application has been revised, please follow' \
                      'the link for more information '
            subject = 'Proposed new loan Amount'
            from_email = 'thronerd@gmail.com'

            try:
                send_mail(subject, message, from_email, [loanapplication.user.email])
            except BadHeaderError:
               messages.error(request,'')
            data['form_is_valid'] = True

        else:
                data['form_is_valid'] = False
    else:
        form = ProposalForm()
    data['html_form'] = render_to_string('includes/proposal-form.html', {'form':form}, request=request)
    return JsonResponse(data)

class AdminloanApplicationView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        amount = self.request.POST.get('amount')
        user = User.objects.get(id=self.request.POST.get('user'))
        loan = self.request.POST.get('loan')
        term = self.request.POST.get('term')
        monthly_payment = self.request.POST.get('monthly_payment')
        total_payment = self.request.POST.get('total_payment')
        last_appID = 0

        for obj in LoanApplication.objects.all():
            last_appID = obj.loanApp_id if obj.loanApp_id > last_appID else last_appID

        loanApp_id = str(timezone.now().year) + str(int(str(last_appID)[4:5])+1)

        loan_calculation_obj = LoanCalculations(amount, loan, term)
        loan = loan_calculation_obj.get_loan()
        loan_details = LoanApplication.objects.create(loanApp_id=loanApp_id, user=user, loan=loan, amount=amount, term=term,
                                                      monthly_payment=monthly_payment, total_payment=total_payment,
                                                      estimated_end_date=timezone.now().date())
        loan_details.save()
        return redirect('dashboard:admin-application-documents')

    def get(self, *args, **kwargs):
        form = LoanApplicationForm()


        context = {
            'form': form
        }
        return render(self.request,'admin-dashboard/Admin-loan-application.html', context)


class AdminApplicationDocumentsView(View):
    def post(self, *args, **kwargs):
        # check if all documents are submitted
        return redirect('dashboard:pending-loans')

    def get(self, *args, **kwargs):
        form = DocumentsForm()
        return render(self.request, 'admin-dashboard/admin-application-documents.html', {'form':form})


def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['tittle', 'description', 'interest'])

    for loan in Loan.objects.all().values_list('tittle', 'description', 'interest'):
        writer.writerow(loan)

    response['Content-Disposition'] = 'attachment; filename="loans.csv"'

    return response


@login_required(login_url="/login/")
def index(request):
    try:
        customer = Customer.objects.get(user=request.user)
        occupation = Occupation.objects.filter(customer = customer)
        bankaccount = BankAccount.objects.filter(customer = customer)

        if not request.user.groups.filter(name='Admin'):
            if customer and bankaccount.exists() and occupation.exists():
                return render(request, "index.html")
            else:
                if customer and not occupation.exists() or not bankaccount.exists():
                    messages.warning(request,
                                     f'Oops! Looks like your occupation or bank information have not been captured,'
                                     f' please complete all field')
                    return redirect('/occupation-and-bank-details/?next=%s' % request.path)
        else:
            return render(request, "index.html")
    except:
        if not request.user.groups.filter(name='Admin'):
            messages.warning(request,
                             f'Oops! Looks like your personal information have not been captured, please complete'
                             f' all field')
            return redirect('/user-details/?next=%s' % request.path)
        else:
            return render(request, "index.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))

class AdminAllLoans(ListView):
    model = LoanApplication
    queryset = LoanApplication.objects.filter(isClosed=False, approved=True)
    paginate_by = 5
    template_name = 'admin-dashboard/all-loans.html'


def adminClosedloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': LoanApplication.objects.filter(isClosed= True)})


def adminWaitingloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': LoanApplication.objects.filter(approved=True, withdrawn=False)})


def adminDeclinedloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': LoanApplication.objects.filter(declined=True)})


def adminWrittenOffloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': LoanApplication.objects.filter(isWrittenoFF=True)})


def adminWithdrawnloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': LoanApplication.objects.filter(withdrawn=True)})


def adminPendingloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': LoanApplication.objects.filter(approved=False, isClosed=False)})

def adminProposedloans(request):
    return render(request, 'loans/status-display.html',
                  {'object_list': ProposedApplication.objects.all()})


def loanDetails(request, id):
    loanapplication = LoanApplication.objects.get(loanApp_id=id)
    if request.POST:
        form = updateLoanForm(request.POST, instance=loanapplication)
        if form.is_valid():
            form.save()
#             massege
            return redirect('dashboard:admin-all-loans')
    else:
        form = updateLoanForm(instance=loanapplication)
        context = {
            'loan_object': loanapplication,
            'borrower_object': Customer.objects.get(user=loanapplication.user),
            'form': form
        }
        return render(request, 'loans/loan-application-details.html', context)


# for admin to add loans using dashboard
class DeclineDocumentView(View):
    def get(self, *args, **kwargs):
        doc_id = self.request.GET.get('doc_id')
        document = Document.objects.get(id = doc_id)
        document.isApproved = False
        document.save()

        get_all_documents = Document.objects.filter(user = document.user)
        temp_doc_list = []
        for obj in get_all_documents:
            temp_doc_list.append(obj.isApproved)

        context = {
            'feedback': 'Updated',
            'all_docs_declined': 'True' if True not in temp_doc_list and None not in temp_doc_list else 'False'
        }
        if context['all_docs_declined'] == 'True':
            messages.info(self.request, f'Application #### is waiting for updated documents')

        return JsonResponse(context)
