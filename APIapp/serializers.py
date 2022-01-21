from rest_framework import serializers

from .models import Company, Transaction


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "status"
        )
        model = Company


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "company_id",
            "price",
            "date",
            "status_transaction",
            "status_approved",
            "final_charge_done"
        )
        model = Transaction