from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework.response import Response
from wallet.services.intra_transfer import wallet_to_wallet_transfer
from .models import Wallet
from .seraializers import WalletTransferSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer_wallet(request):
    sender = request.user.wallet
    serializer = WalletTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data["amount"]
    idempotency_key = serializer.validated_data["idempotency_key"]
    description = serializer.validated_data["description"]
    recipient = get_object_or_404(Wallet, wallet_number=serializer.validated_data["receiver_wallet"])
    tx = wallet_to_wallet_transfer(sender, recipient, amount, idempotency_key, description)

    return Response({
        "amount" : tx.amount,
        "status": tx.status,
        "description": tx.description,
        "created_at": tx.created_at,

    }, status=status.HTTP_201_CREATED)
