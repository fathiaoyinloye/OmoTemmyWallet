from django.dispatch import receiver
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework.response import Response

from services.dashboard_services import get_dashboard_data
from services.user_deposit_service import user_deposit
from wallet.services.intra_transfer import wallet_to_wallet_transfer
from wallet.services.deposit_service import deposit

from .models import Wallet
from .seraializers import WalletTransferSerializer, DashboardSerializer, WalletDepositSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer_wallet(request):
    sender = request.user.wallet
    serializer = WalletTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)


    amount = serializer.validated_data["amount"]
    idempotent_key = serializer.validated_data["idempotent_key"]
    description = serializer.validated_data["description"]
    receiver_wallet = serializer.validated_data["receiver_wallet"]
    recipient = get_object_or_404(Wallet, wallet_number=receiver_wallet.pk)
    tx = wallet_to_wallet_transfer(sender, recipient, amount, idempotent_key, description)

    return Response({
        "amount" : tx.amount,
        "status": tx.status,
        "description": tx.description,
        "created_at": tx.created_at,

    }, status=status.HTTP_201_CREATED)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    dashboard_data = get_dashboard_data(user)
    serializer = DashboardSerializer(dashboard_data)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deposit_wallet(request):
    user_wallet = request.user.wallet
    serializer = WalletDepositSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    amount = serializer.validated_data["amount"]
    idempotent_key = serializer.validated_data["idempotent_key"]
    tx = user_deposit(user_wallet, amount, idempotent_key)
    data = {
        "amount" : tx.amount,
        "status": tx.status,
        "description": tx.description,
    }
    return Response(data, status=status.HTTP_201_CREATED)



