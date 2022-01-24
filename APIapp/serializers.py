from rest_framework import serializers

from .models import Company, Transaction


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "status"
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "company_id",
            "price",
            "date",
            "status_transaction",
            "status_approved",
            "final_charge_done"
        )