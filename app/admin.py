from django.contrib import admin
from loan_management.models import LoanApplication
from import_export.admin import ImportExportModelAdmin


@admin.register(LoanApplication)
class ViewAdmin(ImportExportModelAdmin):
    pass
