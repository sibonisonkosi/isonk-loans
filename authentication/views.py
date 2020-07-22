from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, UserUpdateForm, CustomerDetailsForm, UpdateProfileForm, \
    OccupationForm, BankDetailsForm
from django.views.generic import View
from django.contrib import messages
from .models import Customer, Occupation, BankAccount


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None
    next_url = request.META.get('HTTP_REFERER', '/')
    url = str(next_url).split('/')  # convert the url and store it in the new array variable
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if '?next=' in url: # shot was would be " if request.GET.get('next'):"
                    return redirect(request.GET.get('next'))
                return redirect("dashboard:dashboard-home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created.'
            success = True

            return redirect("login")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


class UserUpdateView(View):
    def post(self, *args, **kwargs):
        form = UserUpdateForm(self.request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Your profile have been successfully updated')
            return redirect('profile')

    def get(self, *args, **kwargs):
        form = UserUpdateForm(instance=self.request.user)
        context = {
            'form': form
        }
        return render(self.request, 'pages/profile.html', context)


class CustomerDetailsView(View):
    def get(self, *args, **kwargs):
        form = CustomerDetailsForm()
        customer_details_exist = Customer.objects.filter(user=self.request.user)

        if customer_details_exist:
            form = CustomerDetailsForm(instance=self.request.user.customer)

        return render(self.request, 'accounts/user-details.html', {'form': form})

    def post(self, *args, **kwargs):
        form = CustomerDetailsForm(self.request.POST)
        customer_details_exist = Customer.objects.filter(user=self.request.user)

        if customer_details_exist:
            form = CustomerDetailsForm(self.request.POST, instance=self.request.user.customer)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = self.request.user
            customer.save()
            # still have to add user feedback

            msg = None
            next_url = self.request.META.get('HTTP_REFERER', '/')
            url = str(next_url).split('/')  # convert the url and store it in the new array variable
            if '?next=' in url:  # shot was would be " if request.GET.get('next'):"
                return redirect(self.request.GET.get('next'))
            return redirect('occupation-and-bank-details')


class OccupationAndBankDetailsView(View):
    def post(self, *args, **kwargs):
        o_form = OccupationForm(self.request.POST)
        b_form = BankDetailsForm(self.request.POST)
        occupation_exist = Occupation.objects.filter(customer=self.request.user.customer)
        bankaccount_exist = BankAccount.objects.filter(customer=self.request.user.customer)

        if occupation_exist:
            o_form = OccupationForm(self.request.POST, instance=self.request.user.customer.occupation)
        if bankaccount_exist:
            b_form = BankDetailsForm(self.request.POST, instance=self.request.user.customer.bankaccount)

        if o_form.is_valid() and b_form.is_valid():
            occupation_details = o_form.save(commit=False)
            occupation_details.customer = self.request.user.customer
            occupation_details.save()

            bank_details = b_form.save(commit=False)
            bank_details.customer = self.request.user.customer
            bank_details.save()
            # Feedback missing

            msg = None
            next_url = self.request.META.get('HTTP_REFERER', '/')
            url = str(next_url).split('/')  # convert the url and store it in the new array variable
            if '?next=' in url:  # shot was would be " if request.GET.get('next'):"
                return redirect(self.request.GET.get('next'))
            return redirect('loan:loan-application')

    def get(self, *args, **kwargs):
        o_form = OccupationForm()
        b_form = BankDetailsForm()
        occupation_exist = Occupation.objects.filter(customer=self.request.user.customer)
        bankaccount_exist = BankAccount.objects.filter(customer=self.request.user.customer)
        if occupation_exist:
            customer = self.request.user.customer
            o_form = OccupationForm(instance=customer.occupation)
        if bankaccount_exist:
            customer = self.request.user.customer
            b_form = BankDetailsForm(instance=customer.bankaccount)

        context = {
            'o_form': o_form,
            'b_form': b_form
        }
        return render(self.request, 'accounts/occupation-and-bank-details.html', context)


class IsIDValildView(View):
    def get(self, *args,**kwargs):
        id_number = self.request.GET.get('id_num')
        a = 0
        b = ''
        c=0
        for i in range(6):
            a += int(id_number[i*2])

        for i in range(6):
            b += id_number[(i*2)+1]
        b = int(b)*2
        for i in range(len(str(b))):
            c += int(str(b)[i])

        a = a+c
        b = str(a)[1]
        a = 10 - int(b)
        isValid = True if a ==int(id_number[12]) else False
        context = {
            'ID_isValid': isValid,
        }
        return JsonResponse(context)


class fomartDOB(View):
    def get(self, *args, **kwargs):
        id_num = self.request.GET.get('id_num', None)

        id_dob = id_num[0:6]
        year = id_dob[0:2]
        month = id_dob[2:4]
        day = id_dob[4:6]
        if int(year) < 50:
            year = '20' + year
        else:
            year = '19' + year

        dob = year + '-' + month + '-' + day

        for_frontend = {
            'DOB': 'invalid' if int(month) >12 or int(day) > 31 else dob,
            'error': True if int(month) > 12 or int(day) > 31 else False
        }
        context = {
            'for_frontend': for_frontend
        }
        return JsonResponse(context)


class isIDExistView(View):
    def get(self, *args, **kwargs):
        context={}
        try:
            id_num = Customer.objects.get(id_num= self.request.GET.get('id_num'))

            context ={'error':True}
        except:
            context ={'error':False}
        return JsonResponse(context)