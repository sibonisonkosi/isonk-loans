from django import forms
from loan_management.models import LoanApplication, Loan, Document, ProposedApplication
from django.contrib.auth.models import User


BOOLEN_CHOICES = (
    (False, 'No'),
    (True, 'Yes'),
)


DOCUMENT_TYPE = (
    ('', '-------'),
    ('Proof of residence', 'Proof of residence'),
    ('Payslip', 'Payslip'),
    ('ID', 'ID'),
    ('Bank statement', 'Bank statement'),
)


class updateLoanForm(forms.ModelForm):
    approved =  forms.ChoiceField(choices=BOOLEN_CHOICES)
    isClosed =  forms.ChoiceField(choices=BOOLEN_CHOICES)
    withdrawn =  forms.ChoiceField(choices=BOOLEN_CHOICES)
    isWrittenoFF =forms.ChoiceField(choices=BOOLEN_CHOICES)
    declined =forms.ChoiceField(choices=BOOLEN_CHOICES)
    declined_and_propose =forms.ChoiceField(choices=BOOLEN_CHOICES)
    class Meta:
        model = LoanApplication
        fields = {
            'approved',
            'isClosed',
            'withdrawn',
            'isWrittenoFF',
            'declined',
            'declined_and_propose',
        }

    def __init__(self, *args, **kwargs):
        super(updateLoanForm, self).__init__(*args, **kwargs)
        self.fields['approved'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['declined_and_propose'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['isClosed'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['withdrawn'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['isWrittenoFF'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['declined'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['declined'].widget.attrs['onchange'] = 'approveDecline()'
        self.fields['approved'].widget.attrs['onchange'] = 'approveDecline()'
        self.fields['isClosed'].widget.attrs['onchange'] = 'disableClose()'
        self.fields['withdrawn'].widget.attrs['onchange'] = 'disableWithdrawn()'
        self.fields['isWrittenoFF'].widget.attrs['onchange'] = 'disableWriteoff()'
        self.fields['declined_and_propose'].widget.attrs['onchange'] = 'proposeNewAmount()'

class UpdateCustomerStatus(forms.ModelForm):
    isClosed = forms.ChoiceField(choices=BOOLEN_CHOICES)

    class Meta:
        model= LoanApplication
        fields={
            'isClosed',
        }

    def __init__(self, *args, **kwargs):
        super(UpdateCustomerStatus, self).__init__(*args, **kwargs)
        self.fields['isClosed'].widget.attrs['class'] = 'form-control form-control-alternative'


class LoanApplicationForm(forms.ModelForm):
    loan = forms.ModelChoiceField(Loan.objects.all())
    user = forms.ModelChoiceField(User.objects.all())
    amount = forms.FloatField(label="")
    term = forms.CharField(label="")
    monthly_payment = forms.CharField(label="",
                                      widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                    'placeholder': '00.0', 'hidden':True}))
    total_payment = forms.CharField(label="",
                                    widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                  'placeholder': '00.0', 'hidden':True}))

    class Meta:
        model = LoanApplication
        fields = {
            'user',
            'loan',
            'amount',
            'term',
            'monthly_payment',
            'total_payment'
        }

    def __init__(self, *args, **kwargs):
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        self.fields['loan'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['user'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['amount'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['term'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['term'].widget.attrs['placeholder'] = 'Term in Months eg: 2'
        self.fields['amount'].widget.attrs['placeholder'] = '00.0'

        self.fields['loan'].widget.attrs['onchange'] = 'loan_calculation()'
        self.fields['term'].widget.attrs['onkeyup'] = 'loan_calculation()'
        self.fields['amount'].widget.attrs['onkeyup'] = 'loan_calculation()'


class ProposalForm(forms.ModelForm):
    loan = forms.ModelChoiceField(Loan.objects.all())
    amount = forms.FloatField(label="")
    term = forms.CharField(label="")
    monthly_payment = forms.CharField(label="",
                                      widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                    'placeholder': '00.0'}))
    total_payment = forms.CharField(label="",
                                    widget=forms.TextInput(attrs={'class': 'form-control form-control-alternative',
                                                                  'placeholder': '00.0'}))

    class Meta:
        model = ProposedApplication
        fields = {
            'loan',
            'amount',
            'term',
            'monthly_payment',
            'total_payment'
        }

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['loan'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['amount'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['term'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['term'].widget.attrs['placeholder'] = 'Term in Months eg: 2'
        self.fields['amount'].widget.attrs['placeholder'] = '00.0'

        self.fields['loan'].widget.attrs['onchange'] = 'loan_calculation()'
        self.fields['loan'].widget.attrs['onclick'] = 'change_background_color()'
        self.fields['term'].widget.attrs['onkeyup'] = 'loan_calculation()'
        self.fields['amount'].widget.attrs['onkeyup'] = 'loan_calculation()'

        self.fields['loan'].widget.attrs['oninput'] = "this.className = ''"
        self.fields['term'].widget.attrs['oninput'] = "this.className = ''"
        self.fields['amount'].widget.attrs['oninput'] = "this.className = ''"


class DocumentsForm(forms.ModelForm):
    doc = forms.FileField(label="", required=False)
    description = forms.CharField(label="", required=False)
    document_type = forms.ChoiceField(label="", choices=DOCUMENT_TYPE, required=False)
    user = forms.ModelChoiceField(User.objects.all(), required=False)

    class Meta:
        model = Document
        exclude = ['hasApplication']

    def __init__(self, *args, **kwargs):
        super(DocumentsForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'form-control form-control-alternative'

        self.fields['doc'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['document_type'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['doc'].widget.attrs['accept'] = '.gif, .jpg, .png, .doc, .pdf'


class newLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'