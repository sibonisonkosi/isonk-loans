from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from loan_management.models import *
from .forms import PaymentForm
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token


class SummaryView(View):
    def get(self, *args, **kwargs):
        form = PaymentForm()
        loanamortization = loanAmortization.objects.filter(user=self.request.user)
        context = {
            'form': form,
            'loan_object': loanamortization if loanamortization.exists() else 'Empty'
        }
        return render(self.request, 'payment_app/summary.html', context)

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        print(self.request.POST)
        try:
            token = self.request.POST.get('stripeToken')
            amount = int(self.request.POST.get('amount'))
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="My First Test Charge (created for API docs)",
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge('id')
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            # calculate the interest paid
            loanapplication = LoanApplication.objects.get(user=self.request.user, withdrawn=True, isClosed=False)
            monthy_payment_with_interest = loanapplication.monthly_payment
            monthy_payment_with_no_interest = loanapplication.amount / loanapplication.term

            # assign payment to loanAmortization
            loanamortization = loanAmortization.objects.get(loanapplication=loanapplication)
            loanamortization.payment = payment
            loanamortization.payment_date = timezone.now().date()
            loanamortization.payment_amount = amount
            loanamortization.interest_paid = monthy_payment_with_interest - monthy_payment_with_no_interest
            loanamortization.principle_paid = loanamortization.principle_paid + amount
            loanamortization.ending_balance = loanamortization.ending_balance - amount
            loanamortization.save()
            messages.info(self.request, 'Your payment was successful! Amount paid will reflect after 24 hours')
            return redirect('loan_payment:payment-summary')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('loan_payment:payment-summary')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, f"Rate Limit Error")
            return redirect('loan_payment:payment-summary')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, f"Invalid Request Error")
            return redirect('loan_payment:payment-summary')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, f"Not Authentication")
            return redirect('loan_payment:payment-summary')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, f"Network Error")
            return redirect('loan_payment:payment-summary')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, f"Something went wrong. You were not charged. Please try again")
            return redirect('loan_payment:payment-summary')

        except Exception as e:
            # send and email to ourselves
            messages.error(self.request, f"A serious error occurred we have been notified ")
            return redirect('loan_payment:payment-summary')

class PaymentView(TemplateView):
    template_name = 'payment_app/payment-page.html'