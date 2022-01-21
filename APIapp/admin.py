from django.contrib import admin

from .models import Company, Transaction


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status"
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_id",
        "price",
        "date",
        "status_transaction",
        "status_approved",
        "final_charge_done"
    )


admin.site.register(Company, CompanyAdmin)
admin.site.register(Transaction, TransactionAdmin)