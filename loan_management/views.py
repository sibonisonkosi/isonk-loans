from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from .forms import LoanApplicationForm, DocumentsForm
from .logic import LoanCalculations
from .models import LoanApplication, Loan, Document, loanAmortization, ProposedApplication
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from core.forms import updateLoanForm, UpdateCustomerStatus


class loanApplicationView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):

        all_documents_uploaded = False
        document = Document.objects.filter(user=self.request.user)  # still have to filter by date or use boolen field
        doc = []
        for a in document:
            doc.append(a.document_type)
        all_documents_uploaded = True if 'ID' in doc and 'Payslip' in doc and 'Prof of residence' \
                                         and 'Bank statement' in doc else False
        if all_documents_uploaded:
            amount = self.request.POST.get('amount')
            loan = self.request.POST.get('loan')
            term = self.request.POST.get('term')
            monthly_payment = self.request.POST.get('monthly_payment')
            total_payment = self.request.POST.get('total_payment')
            user = self.request.user
            last_appID = 0
            if LoanApplication.objects.all().count() > 0:
                for obj in LoanApplication.objects.all():
                    last_appID = obj.pk if obj.pk > last_appID else last_appID

            loanApp_id = 20201 if last_appID == 0 else last_appID +1

            loan_calculation_obj = LoanCalculations(amount, loan, term)
            loan = loan_calculation_obj.get_loan()
            loan_details = LoanApplication.objects.create(loanApp_id=loanApp_id,user=user, loan=loan, amount=amount,
                                                          term=term,monthly_payment=monthly_payment,
                                                          total_payment=total_payment,
                                                          estimated_end_date=loan_calculation_obj.get_estimated_end_date())
            loan_details.save()

            messages.success(self.request, f'Congratulations! You have place your loan application.')
            return redirect('loan:pending-loans')
        else:
            messages.warning(self.request, f'Please ensure all required documents are uploaded')
            l_form = LoanApplicationForm(self.request.POST)
            d_form = DocumentsForm(self.request.POST)
            context = {
                'l_form': l_form,
                'd_form': d_form,
            }
            return render(self.request, 'loans/new-loan.html', context)

    def get(self, *args, **kwargs):
        application = LoanApplication.objects.filter(user=self.request.user, approved=False, isClosed=False)

        if not application.exists():

            if self.request.user.customer:
                l_form = LoanApplicationForm()
                d_form = DocumentsForm()
                context = {
                    'l_form': l_form,
                    'd_form': d_form,
                }
                return render(self.request, 'loans/new-loan.html', context)
        else:
            messages.info(self.request, f'Sorry you cannot place another application you still have pending application')
            return redirect('loan:pending-loans')


class MyLoansView(ListView):
    model = LoanApplication
    template_name = 'loans/my_loan.html'

    def get_queryset(self):
        return LoanApplication.objects.filter(user=self.request.user, approved=True, isClosed=False)


def Closedloans(request):
    context = {
        'object_list': LoanApplication.objects.filter(user= request.user, isClosed= True,),
        'page': 'Closed'
    }
    return render(request, 'loans/status-display.html',context)


def Waitingloans(request):
    context ={
        'object_list': LoanApplication.objects.filter(user= request.user, approved=True, withdrawn=False),
        'page': 'Waiting'
    }
    return render(request, 'loans/status-display.html',context)


def Declinedloans(request):
    context = {
        'object_list': LoanApplication.objects.filter(user= request.user, declined=True),
        'page': 'Declined'
       }
    return render(request, 'loans/status-display.html',context)


def WrittenOffloans(request):
    context = {
        'object_list': LoanApplication.objects.filter(user= request.user, isWrittenoFF=True),
        'page': 'Written Off'
    }
    return render(request, 'loans/status-display.html',context)


def Proposedloan(request):
    context = {
        'object_list': ProposedApplication.objects.filter(user= request.user),
        'page': 'Proposed'
    }
    return render(request, 'loans/status-display.html',context)


def Pendingloans(request):
    context ={
        'object_list': LoanApplication.objects.filter(user= request.user, approved=False, isClosed=False),
        'page': 'Pending'
    }
    return render(request, 'loans/status-display.html', context)

def loanDetails(request, id):
    loanapplication = LoanApplication.objects.get(loanApp_id=id)
    if request.POST:
        if request.user.groups.filter(name='Admin'):
            messages.success(request, f'Loan application status has been successfully updated')
            form = updateLoanForm(request.POST, instance=loanapplication)
        else:
            messages.success(request, f'Loan application has been successfully cancelled')
            form = UpdateCustomerStatus(request.POST, instance=loanapplication)
        if form.is_valid():
            if not request.user.groups.filter(name='Admin'):
                cancel = form.cleaned_data.get('isClosed')
                if cancel:
                    close_status = form.save(commit=False)
                    close_status.approved = False
                    close_status.withdrawn = False
                    close_status.isWrittenoFF = False
                    close_status.declined = False
                    close_status.declined_and_propose = False
                    close_status.save()
            else:
                form.save()
            return redirect('dashboard:admin-all-loans')
    else:
        if request.user.groups.filter(name='Admin'):
            form = updateLoanForm(instance=loanapplication)
        else:
            form = UpdateCustomerStatus(instance=loanapplication)
        context = {
            'loan_object': loanapplication,
            'form': form,
            'documents': Document.objects.filter(user=loanapplication.user)
        }
        return render(request, 'loans/loan-application-details.html', context)


def AcceptProposal(request, id):
    proposedapplication = ProposedApplication.objects.get(id=id)
    update_application_loan = LoanApplication.objects.get(loanApp_id =proposedapplication.loanapplication.loanApp_id)
    update_application_loan.isClosed = False
    update_application_loan.isWrittenoFF = False
    update_application_loan.approved = True
    update_application_loan.declined_and_propose = False
    update_application_loan.withdrawn = False
    update_application_loan.declined = False
    update_application_loan.save()

    proposedapplication.delete()
    return redirect('loan:my-loans')


def RejectProposal(request, id):
    proposedapplication = ProposedApplication.objects.get(id=id)
    update_application_loan = LoanApplication.objects.get(loanApp_id =proposedapplication.loanapplication.loanApp_id)
    update_application_loan.isClosed = True
    update_application_loan.isWrittenoFF = False
    update_application_loan.approved = False
    update_application_loan.declined_and_propose = True
    update_application_loan.withdrawn = False
    update_application_loan.declined = True
    update_application_loan.save()

    proposedapplication.delete()
    return redirect('loan:my-loans')

def withdrawLoan(request, id):
    loanapplication = LoanApplication.objects.get(loanApp_id=id)
    loanapplication.withdrawn = True

    loanamortization = loanAmortization.objects.create(
        user= loanapplication.user,
        loan_application= loanapplication,
        payment_date = timezone.now().date(),
        starting_balance = loanapplication.total_payment,
        payment_amount = 0,
        interest_paid = 0,
        principle_paid = 0,
        ending_balance = loanapplication.total_payment
    )
    loanamortization.save()
    loanapplication.save()
    return redirect('loan:my-loans')

def cancelLoan(request, id):
    loanapplication = LoanApplication.objects.get(loanApp_id=id)
    # before canceling must ask the borrower to confirm
    loanapplication.isClosed = True
    loanapplication.save()
    return redirect('loan:my-loans')


# On change control used by json to get loan calculations to display for the user
class get_loan_calculations(View):
    def get(self, *args, **kwargs):
        term = int(self.request.GET.get('term', None))
        amount = float(self.request.GET.get('amount', None))
        loan = self.request.GET.get('loan', None)
        loan_calculation_obj = LoanCalculations(amount, loan, term)

        total_payment = loan_calculation_obj.total_payment_with_interest()
        monthly_payment = loan_calculation_obj.cal_mothly_payment()

        for_frontend = {
            'total_payment': str(round(total_payment, 2)),
            'monthly_payment': str(round(monthly_payment, 2))
        }
        context = {
            'for_frontend': for_frontend
        }
        return JsonResponse(context)


# Json controller used to upload required documents.
class saveDocumentView(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        file = self.request.FILES.getlist('file')[0]
        description = self.request.POST.get('description')
        document_type = self.request.POST.get('document_type')
        document = Document.objects.create(user=self.request.user,
                                           document_type=document_type, description=description, doc=file)
        get_doc_id = document
        doc_id = get_doc_id.id
        document.save()

        file_name = file.name[0:25] + ' ...' if len(file.name) > 25 else file.name
        context = {
            'error': False,
            'name': file_name,
            'doc_type': document_type,
            'get_doc_id': doc_id
        }
        return JsonResponse(context)

    def get(self, *args, **kwargs):
        d_form = DocumentsForm()
        context = {
            'd_form': d_form
        }
        return render(self.request, 'loans/save-document.html', context)


class DisplyDocuments(View):
    def get(self, *args, **kwargs):
        doc_type = self.request.GET.get('doc_type')
        documents = Document.objects.filter(user=self.request.user,document_type = doc_type, hasApplication=False)
        get_doc = documents[0]
        doc_id = get_doc.id

        file_name = get_doc.doc.name[0:25] + ' ...' if len(get_doc.doc.name) > 25 else get_doc.doc.name
        context = {
            'error': False,
            'name': file_name,
            'doc_type': get_doc.document_type,
            'get_doc_id': doc_id
        }
        return JsonResponse(context)


class removeDocument(View):
    def get(self, *args, **kwargs):
        document_id = self.request.GET.get('document_id')
        document = Document.objects.get(pk=document_id)
        document.delete()
        messages.success(self.request, f'Document successfully removed!')
        context = {
            'feedback': 'Done'
        }
        return JsonResponse(context)


class allDocumentsUploaded(View):
    def get(self, *args, **kwargs):
        all_documents_uploaded = False
        document = Document.objects.filter(user=self.request.user)  # still have to filter by date or use boolen field
        doc = []
        for a in document:
            doc.append(a.document_type)
        all_documents_uploaded = True if 'ID' in doc and 'Payslip' in doc and 'Prof of residence' \
                                         and 'Bank statement' in doc else False
        return JsonResponse({'isUploaded': all_documents_uploaded})

class LoanApplicationSummaryView(View):
    def get(self, *args, **kwargs):
        loan_details =get_object_or_404(LoanApplication, user=self.request.user)
        context = {
            'loan_details': loan_details
         }
        return render(self.request, 'loans/loan-application-summary.html', context)


