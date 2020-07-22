from .models import LoanApplication, Loan
from django.utils import timezone
import calendar


class LoanCalculations:

    def __init__(self, amount, loan, term):
        self.amount = amount
        self.loan = loan
        self.term = term

    def cal_mothly_payment(self):
        total_payment = self.total_payment_with_interest()
        payment = total_payment / self.term
        return payment

    def total_payment_with_interest(self):
        return self.amount + (self.amount * self.get_interest())

    def get_loan(self):
        return Loan.objects.get(pk=self.loan)

    def get_interest(self):
        interest = self.get_loan().interest / 100
        return interest

    def get_estimated_end_date(self):
        application_date = timezone.now().date()
        estimated_month = int(application_date.month) + int(self.term)
        estimated_year = int(application_date.year)

        if estimated_month > 12:
            estimated_year += 1
            estimated_month -= 12
        estimated_day = calendar.monthrange(estimated_year, estimated_month)[1]
        return str(estimated_year) + '-' + str(estimated_month) + '-' + str(estimated_day)
