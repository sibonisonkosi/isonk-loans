from django import forms

PAYMENT_TYPE = (
    ('Stripe', 'Stripe'),
    ('Paypal', 'Paypal')
)
class PaymentForm(forms.Form):
    amount = forms.CharField()
    payment_type = forms.ChoiceField(choices=PAYMENT_TYPE)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['class'] = 'form-control form-control-alternative'
        self.fields['payment_type'].widget.attrs['class'] = 'form-control form-control-alternative'