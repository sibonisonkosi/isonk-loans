from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages


class indexView(TemplateView):
    template_name = 'app/index.html'


class aboutView(TemplateView):
    template_name = 'app/about.html'


class contactView(View):
    def post(self, *args, **kwargs):
        form = ContactForm(self.request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['sibonisonkosi95@gmail.com'])
            except BadHeaderError:
                return render(self.request, 'app/contact.html', {'form': form})
            messages.success(self.request, f'Email sent successfully. Thank you!')
            return redirect('app:contact')
        return render(self.request, 'app/contact.html', {'form': form})

    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(self.request, 'app/contact.html', context)


