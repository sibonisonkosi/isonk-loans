from django import template
from loan_management.models import LoanApplication

register = template.Library()

# @register.simple_tag
@register.inclusion_tag('includes/admin-loans-header.html')
def admin_get_loan_data():
    written_off_loans = LoanApplication.objects.filter(isWrittenoFF=True)
    withdrawn_loans = LoanApplication.objects.filter(withdrawn=True)
    declined_loans = LoanApplication.objects.filter(declined=True)
    closed_loans = LoanApplication.objects.filter(isClosed=True)
    waiting_loans = LoanApplication.objects.filter(approved=True)
    pending_loans = LoanApplication.objects.filter(approved=False, isClosed=False)
    context = {
        'written_off_loans': written_off_loans.count(),
        'withdrawn_loans': withdrawn_loans.count(),
        'declined_loans': declined_loans.count(),
        'closed_loans': closed_loans.count(),
        'waiting_loans': waiting_loans.count(),
        'pending_loans': pending_loans.count(),
    }
    return context