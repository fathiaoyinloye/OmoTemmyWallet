from rest_framework import serializers
from wallet.models import Wallet


class WalletTransferSerializer(serializers.Serializer):
    receiver_wallet = serializers.CharField(max_length=10, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField(required=True)

    def validate_amount(self, amount):
        if amount > 0:
            raise Exception("Amount must be greater than 0")
        return amount

    def validate_receiver_wallet(self, receiver_wallet):
        try:
            wallet = Wallet.objects.get(pk=receiver_wallet)
        except Wallet.DoesNotExist:
            raise Exception("Wallet does not exist")
        return wallet