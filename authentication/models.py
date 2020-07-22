from PIL import Image
from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICE = (
    ('F', 'Female'),
    ('M', 'Male'),
)

PROVINCE_CHOICE = (
    ('KZN', 'KwaZulu Natal'),
    ('GP', 'Guateng'),
    ('LM', 'Limpopo'),
    ('WC', 'Western Cape'),
    ('MP', 'Mpumalanga'),
    ('FS', 'Free State'),
    ('NC', 'Northern Cape'),
    ('EC', 'Eastern Cape'),
    ('NW', 'North West'),

)


# This will hold user extra information like contact details
class Customer(models.Model):
    id_num = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    phone_no = models.CharField(max_length=12)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=1)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICE)

    class Meta:
        verbose_name_plural = 'Customers'
        ordering = ('user', 'id_num')

    def __str__(self):
        return f'{self.user.username} Customer'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='default.jpg', blank=True, upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class BankAccount(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="bankaccount")
    bank_name = models.CharField(verbose_name='Name of the bank', max_length=200)
    account_type = models.CharField(verbose_name='Account type', max_length=200)
    account_num = models.BigIntegerField()

    class Meta:
        verbose_name_plural = 'Bank Accounts'
        ordering = ('account_num', 'bank_name',)

    def __str__(self):
        return self.customer.user.username


# user working information associated with the customer will be captured by this table
class Occupation(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="occupation")
    employer = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    telephone_num = models.CharField(max_length=10)

    def __str__(self):
        return self.customer.user.username
