from django.contrib.admin import ModelAdmin, register
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Customer, Occupation, BankAccount, Profile


@register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ('user', 'phone_no', 'gender', 'dob',)
    icon_name = 'person_outline'


@register(Profile)
class ProfileAdmin(ModelAdmin):
    icon_name = 'person_outline'


@register(Occupation)
class OccupationAdmin(ModelAdmin):
    list_display = ('customer', 'employer',)
    icon_name = 'work'


@register(BankAccount)
class BankAccountAdmin(ModelAdmin):
    list_display = ('customer', 'bank_name', 'account_num',)
    icon_name = 'account_balance'