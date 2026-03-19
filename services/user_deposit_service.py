from decimal import Decimal
from uuid import UUID

from rest_framework.generics import get_object_or_404

from wallet.models import Wallet
from wallet.seraializers import WalletTransferSerializer
from wallet.services.deposit_service import deposit
from notification.services import create_deposit_notification
def user_deposit(user_wallet: Wallet, amount: Decimal, idempotent_key: UUID):
    tx = deposit(user_wallet, amount, idempotent_key)
    updated_wallet = get_object_or_404(Wallet, wallet_number=user_wallet.pk)
    create_deposit_notification(updated_wallet, amount)
    return tx