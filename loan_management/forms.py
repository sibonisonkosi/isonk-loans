from django import forms
from .models import LoanApplication, Loan, Document

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

'''
    Below are forms to capture new loan application details 
'''


class DocumentsForm(forms.Form):
    doc = forms.FileField(label="")
    description = forms.CharField(label="")
    document_type = forms.ChoiceField(label="", choices=DOCUMENT_TYPE)

    def __init__(self, *args, **kwargs):
        super(DocumentsForm, self).__init__(*args, **kwargs)
        self.fields['doc'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['document_type'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['doc'].widget.attrs['accept'] = '.gif, .jpg, .png, .doc, .pdf'


class LoanApplicationForm(forms.ModelForm):
    loan = forms.ModelChoiceField(Loan.objects.all())
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
            'loan',
            'amount',
            'term',
            'monthly_payment',
            'total_payment'
        }

    def __init__(self, *args, **kwargs):
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        self.fields['loan'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['amount'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['term'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['term'].widget.attrs['placeholder'] = 'Term in Months eg: 2'
        self.fields['amount'].widget.attrs['placeholder'] = '00.0'

        self.fields['loan'].widget.attrs['onchange'] = 'loan_calculation()'
        self.fields['term'].widget.attrs['onkeyup'] = 'loan_calculation()'
        self.fields['amount'].widget.attrs['onkeyup'] = 'loan_calculation()'


class DocumentsForm(forms.Form):
    doc = forms.FileField(label="", required=False)
    description = forms.CharField(label="", required=False)
    document_type = forms.ChoiceField(label="", choices=DOCUMENT_TYPE, required=False)

    def __init__(self, *args, **kwargs):
        super(DocumentsForm, self).__init__(*args, **kwargs)
        self.fields['doc'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['document_type'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['doc'].widget.attrs['accept'] = '.gif, .jpg, .png, .doc, .pdf'

        self.fields['description'].widget.attrs['placeholder'] = 'Description'

