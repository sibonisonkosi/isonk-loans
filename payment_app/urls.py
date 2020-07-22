from django.urls import path
from . import views

app_name = 'loan_payment'
urlpatterns = [
    path('payment/summary', views.SummaryView.as_view(), name='payment-summary'),
    path('payment/pay', views.PaymentView.as_view(), name='payment'),
]