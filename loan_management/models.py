from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import calendar


DOCUMENT_TYPE = (
    ('Proof of residence', 'Proof of residence'),
    ('Payslip', 'Payslip'),
    ('ID', 'ID'),
    ('Bank statement', 'Bank statement'),
)

LOAN_TYPE = (
    ('PL', 'Personal Loan'),
    ('SL', 'Secured Loan'),
    ('PDL', 'Payday Loan'),
    ('DCL', 'Debt consolidation loans'),
    ('BCL', 'Bad credit loans'),
)

TERM_CHOICE = (
    ('6', '6'),
    ('12', '12'),
    ('24', '24'),
    ('36', '36'),
    ('48', '48'),
)


class Loan(models.Model):
    tittle = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    interest = models.FloatField()

    class Meta:
        verbose_name_plural = 'Loans'
        ordering = ('interest',)

    def __str__(self):
        return self.tittle

    def get_absolute_url(self):
        return reverse('dashboard:Admin-loans')


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class LoanApplication(models.Model):
    loanApp_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loanapplications',
                             related_query_name='loanapplication')

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField()
    term = models.CharField(max_length=20)
    monthly_payment = models.FloatField()
    total_payment = models.FloatField()
    estimated_end_date = models.DateField()
    application_date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    withdrawn = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    declined_and_propose = models.BooleanField(default=False)
    isWrittenoFF = models.BooleanField(default=False)
    isClosed = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse("loan:loan-deatils", kwargs={
            'id': self.loanApp_id
        })

    def get_withdraw_url(self):
        return reverse("loan:withdraw-loan", kwargs={
            'id': self.loanApp_id
        })

    def get_cancel_url(self):
        return reverse("loan:cancel-loan", kwargs={
            'id': self.loanApp_id
        })

    class Meta:
        verbose_name_plural = 'Loans Applications'
        ordering = ('approved', 'application_date', 'amount',)

    def __str__(self):
        return self.user.username


class ProposedApplication(models.Model):
    loanapplication = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='proposedapplication', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField()
    term = models.CharField(max_length=20)
    monthly_payment = models.FloatField()
    total_payment = models.FloatField()
    application_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    # Stiil to change this
    def Accept_url(self):
        return reverse("loan:accept-proposal", kwargs={
            'id': self.id
        })

    def Reject_and_close_url(self):
        return reverse("loan:reject-proposal", kwargs={
            'id': self.id
        })

    class Meta:
        verbose_name_plural = 'Proposed Applications'
        ordering = ('application_date', 'amount',)

    def __str__(self):
        return self.user.username


# class ApprovedLoan(models.Model):
#     approved_loan_id = models.IntegerField(primary_key=True)
#     loanapplication = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='approvedloan')
#

# Loan Amortization is a complete table of periodic loan payments, showing the amount of loan principle and
# the amount of interest that comprise each payment until the balance of loan is zero at the end of it term
# In the context of borrowing, principal refers to the initial size of a loan; it can also mean the amount
# still owed on a loan. If you take out a $50,000 mortgage, for example, the principal is $50,000.
# If you pay off $30,000, the principal balance now consists of the remaining $20,000.
class loanAmortization(models.Model):
    user = user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='loanamortization')
    payment_date = models.DateField()
    starting_balance = models.FloatField()
    payment_amount = models.FloatField()
    interest_paid = models.FloatField()
    principle_paid = models.FloatField()
    ending_balance = models.FloatField()

    class Meta:
        verbose_name_plural = 'Loan Amortizations'
        ordering = ('ending_balance',)

    def __str__(self):
        return f'{self.loan_application.id} by {self.loan_application.user.username}'


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(choices=DOCUMENT_TYPE, max_length=50)
    description = models.CharField(max_length=50, default="Bank Statement, Proof of Residence, Payslip, ID Document")
    doc = models.FileField(upload_to='documents', null=True, blank=True)
    isApproved = models.NullBooleanField()
    last_updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class LoanAplicationDocument(models.Model):
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.loan_application.user.username
