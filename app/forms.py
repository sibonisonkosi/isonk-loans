from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-100', 'id': 'message',
                                                           'cols': '30', 'rows': '9', 'placeholder': 'Enter Message'}),
                              required=True)

    from_email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email address'})
    subject.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Subject'})
