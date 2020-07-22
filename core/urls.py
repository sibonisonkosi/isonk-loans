from django.urls import path, re_path
from . import views

app_name = "dashboard"
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('dashboard-home', views.index, name='dashboard-home'),
    path('dashboard/admin-all-loans/', views.AdminAllLoans.as_view(), name='admin-all-loans'),
    path('dashboard/admin-closed-loans/', views.adminClosedloans, name='closed-loans'),
    path('dashboard/admin-written-off-loans/', views.adminWrittenOffloans, name='written-off-loans'),
    path('dashboard/admin-withdrawn-loans/', views.adminWithdrawnloans, name='withdrawn-loans'),
    path('dashboard/admin-proposed-loans/', views.adminProposedloans, name='proposed-loans'),
    path('dashboard/admin-pending-loans/', views.adminPendingloans, name='pending-loans'),
    path('dashboard/admin-waiting-loans/', views.adminWaitingloans, name='waiting-loans'),
    path('dashboard/admin-declined-loans/', views.adminDeclinedloans, name='declined-loans'),
    path('dashboard/loan-deatils/<id>', views.loanDetails, name='loan-deatils'),
    path('dashboard/create-loan/', views.CreateLoanTest.as_view(), name='create-loan'),
    path('dashboard/Admin-loans', views.AdminViewLoans.as_view(), name='Admin-loans'),
    path('dashboard/admin-loan-application/', views.AdminloanApplicationView.as_view(), name='admin-loan-application'),
    path('dashboard/admin-application-documents/', views.AdminApplicationDocumentsView.as_view(),
         name='admin-application-documents'),
    path('export/', views.export, name='export'),
    path('decline-document/', views.DeclineDocumentView.as_view(), name='decline-document'),
    path('dashboard/application-proposal/', views.ProposalView, name='application-proposal'),
]
