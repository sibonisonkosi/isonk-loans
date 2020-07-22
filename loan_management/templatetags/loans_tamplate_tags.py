from django import template
from loan_management.models import LoanApplication, ProposedApplication

register = template.Library()

# @register.simple_tag
@register.inclusion_tag('includes/my-loans-header.html')
def get_loan_data(user):
    written_off_loans = LoanApplication.objects.filter(user=user, isWrittenoFF=True)
    declined_loans = LoanApplication.objects.filter(user=user, declined=True)
    closed_loans = LoanApplication.objects.filter(user=user, isClosed=True)
    waiting_loans = LoanApplication.objects.filter(user=user, approved=True, withdrawn=False)
    pending_loans = LoanApplication.objects.filter(user=user, approved=False, isClosed=False)
    declined_and_proposed_loans = ProposedApplication.objects.filter(user=user)
    context = {
        'written_off_loans': written_off_loans.count(),
        'declined_loans': declined_loans.count(),
        'closed_loans': closed_loans.count(),
        'waiting_loans': waiting_loans.count(),
        'pending_loans': pending_loans.count(),
        'declined_and_proposed': declined_and_proposed_loans.count(),
    }
    return context