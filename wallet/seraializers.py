from rest_framework import serializers
from wallet.models import Wallet, Transaction


class WalletTransferSerializer(serializers.Serializer):
    receiver_wallet = serializers.CharField(max_length=10, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotent_key = serializers.UUIDField(required=True)
    description = serializers.CharField(max_length= 225, required= False)

    def validate_amount(self, amount):
        if amount < 0:
            raise Exception("Amount must be greater than 0")
        return amount

    def validate_receiver_wallet(self, receiver_wallet):
        try:
            wallet = Wallet.objects.get(pk=receiver_wallet)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet does not exist")
        return wallet

class RecentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['receiver', 'reference', 'amount', 'status', 'created_at', 'transaction_type']


class DashboardSerializer(serializers.Serializer):
    message = serializers.CharField(max_length= 55)
    wallet = serializers.CharField(max_length=10)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length= 3)
    status = serializers.CharField(max_length= 10)
    transactions = RecentTransactionSerializer(many=True)


class WalletDepositSerializer(serializers.Serializer):
    wallet = serializers.CharField(max_length=10, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotent_key = serializers.UUIDField(required=True)

    def validate_amount(self, amount):
        if amount < 0:
            raise Exception("Amount must be greater than 0")
        return amount





