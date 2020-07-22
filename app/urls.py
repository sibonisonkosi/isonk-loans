from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "app"
urlpatterns = [
    path('', views.indexView.as_view(), name='home'),
    path('contact/', views.contactView.as_view(), name='contact'),
    path('about/', views.aboutView.as_view(), name='about'),
]