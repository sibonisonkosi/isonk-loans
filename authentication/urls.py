from django.urls import path
from .views import login_view, register_user, UserUpdateView, CustomerDetailsView, OccupationAndBankDetailsView, \
    IsIDValildView, fomartDOB, isIDExistView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('user-details/', CustomerDetailsView.as_view(), name='user-details'),
    path('occupation-and-bank-details/', OccupationAndBankDetailsView.as_view(), name='occupation-and-bank-details'),
    path('is-ID-valid/', IsIDValildView.as_view(), name='is-ID-valid'),
    path('format-dob/', fomartDOB.as_view(), name='format-dob'),
    path('is-ID-exists/', isIDExistView.as_view(), name='is-ID-exists'),
]