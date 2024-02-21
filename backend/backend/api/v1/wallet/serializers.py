from rest_framework import serializers

from api.v1.accounts.serializers import CustomUserSerializer
from apps.wallet.models import EmployeeWallet, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'date',
            'description',
        ]


class EmployeeWalletSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = EmployeeWallet
        fields = [
            "id",
            "user",
            "balance",
            "transactions"
        ]
