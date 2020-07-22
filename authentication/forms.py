from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Profile, Occupation, BankAccount

PROVINCE_CHOICE = (
    ('', 'Select Province'),
    ('KZN', 'KwaZulu Natal'),
    ('GP', 'Guateng'),
    ('LM', 'Limpopo'),
    ('WC', 'Western Cape'),
    ('MP', 'Mpumalanga'),
    ('FS', 'Free State'),
    ('NC', 'Northern Cape'),
    ('EC', 'Eastern Cape'),
    ('NW', 'North West'),

)

DOCUMENT_TYPE = (
    ('', '-------'),
    ('Proof of residence', 'Proof of residence'),
    ('Payslip', 'Payslip'),
    ('ID', 'ID'),
    ('Bank statement', 'Bank statement'),
)

GENDER_CHOICE = (
    ('', 'select gender'),
    ('F', 'Female'),
    ('M', 'Male')
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['username'].widget.attrs['id'] = 'input-username'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'input-email'
        self.fields['username'].widget.attrs['placeholder'] = 'Email address'

        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['first_name'].widget.attrs['id'] = 'input-first-name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['last_name'].widget.attrs['id'] = 'input-last-name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'image'}

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs['class'] = 'form-control form-control-alternative'


class CustomerDetailsForm(forms.ModelForm):
    id_num = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                        'placeholder': 'ID Number',
                                                                        'required': True}))

    gender = forms.ChoiceField(label="", choices=GENDER_CHOICE)
    dob = forms.DateField(label="")
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                   'placeholder': 'city',
                                                                   'required': True}))
    province = forms.ChoiceField(label="", choices=PROVINCE_CHOICE)
    phone_no = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                       'label': '', 'placeholder': 'phone number',
                                                                       'required': True}))
    postal_code = forms.CharField()

    class Meta:
        model = Customer
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(CustomerDetailsForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['address'].widget.attrs['placeholder'] = 'Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09'
        self.fields['address'].widget.attrs['required'] = True

        self.fields['gender'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['gender'].widget.attrs['required'] = True

        self.fields['postal_code'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Postal code'

        self.fields['province'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['province'].widget.attrs['required'] = True

        self.fields['dob'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['dob'].widget.attrs['required'] = True
        self.fields['dob'].widget.attrs['placeholder'] = 'Date of birth'
        self.fields['dob'].widget.attrs['disabled'] = False


class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
        super(BankDetailsForm, self).__init__(*args, **kwargs)
        self.fields['account_num'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['account_type'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['bank_name'].widget.attrs['class'] = 'form-control form-control-alternative'


class OccupationForm(forms.ModelForm):
    class Meta:
        model = Occupation
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
            super(OccupationForm, self).__init__(*args, **kwargs)
            self.fields['employer'].widget.attrs['class'] = 'form-control form-control-alternative'
            self.fields['position'].widget.attrs['class'] = 'form-control form-control-alternative'
            self.fields['telephone_num'].widget.attrs['class'] = 'form-control form-control-alternative'

