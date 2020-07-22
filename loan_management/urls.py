from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'loan'
urlpatterns = [
    path('loan-application/', views.loanApplicationView.as_view(), name='loan-application'),
    path('get-loan-calculations/', views.get_loan_calculations.as_view(), name='get-loan-calculations'),
    path('remove-document/', views.removeDocument.as_view(), name='remove-document'),
    path('save-document/', views.saveDocumentView.as_view(), name='save-document'),
    path('loan-application-summary/', views.LoanApplicationSummaryView.as_view(), name='loan-application-summary'),
    path('display-document/', views.DisplyDocuments.as_view(), name='display-document'),
    path('all-documents-uploaded/', views.allDocumentsUploaded.as_view(), name='all-documents-uploaded'),
    path('my-loans/', views.MyLoansView.as_view(), name='my-loans'),

    path('closed-loans/', views.Closedloans, name='closed-loans'),
    path('written-off-loans/', views.WrittenOffloans, name='written-off-loans'),
    path('proposed-loan/', views.Proposedloan, name='proposed-loan'),
    path('pending-loans/', views.Pendingloans, name='pending-loans'),
    path('waiting-loans/', views.Waitingloans, name='waiting-loans'),
    path('declined-loans/', views.Declinedloans, name='declined-loans'),
    path('loan-deatils/<id>', views.loanDetails, name='loan-deatils'),

    path('loan-deatils/<id>', views.loanDetails, name='loan-deatils'),
    path('accept-proposal/<id>', views.AcceptProposal, name='accept-proposal'),
    path('reject-proposal/<id>', views.RejectProposal, name='reject-proposal'),

    path('cancel-loan/<id>', views.cancelLoan, name='cancel-loan'),
    path('withdraw-loan/<id>', views.withdrawLoan, name='withdraw-loan'),
]
