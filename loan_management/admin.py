from django.contrib.admin import ModelAdmin, register
from django.contrib import admin
from .models import Loan, LoanApplication, Document, loanAmortization, ProposedApplication


@register(loanAmortization)
class LoanAmortizationAdmin(ModelAdmin):
    list_display = ('user', 'payment_date','starting_balance', 'payment_amount', 'interest_paid', 'principle_paid',
                    'ending_balance')
    icon_name = 'payment'


@register(Loan)
class LoanAdmin(ModelAdmin):
    list_display = ('tittle', 'description',)
    icon_name = 'monetization_on'


@register(LoanApplication)
class LoanApplicationAdmin(ModelAdmin):
    list_display = ('user', 'term', 'amount',)
    icon_name = 'assessment'

@register(ProposedApplication)
class ProposedApplicationAdmin(ModelAdmin):
    list_display = ('loanapplication', 'term', 'amount',)
    icon_name = 'assessment'


@register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ('user', 'document_type', 'description',)
    icon_name = 'attach_file'
