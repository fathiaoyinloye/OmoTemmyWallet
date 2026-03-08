from decimal import Decimal
from uuid import UUID

from wallet.models import Wallet, Transaction, Ledger
from django.db import transaction


def wallet_to_wallet_transfer(sender: Wallet, receiver: Wallet, amount: Decimal, idempotent_key: UUID, description: str=None):
    if sender.pk == receiver.pk:
        raise Exception("sender and receiver cannot be the same")
    if amount > sender.balance:
        raise Exception("Insufficient balance")
    existing_tx = Transaction.objects.filter(idempotent_key = idempotent_key).first()
    if existing_tx:
        return existing_tx
    with transaction.atomic():
        try:
            receiver_wallet = Wallet.objects.select_for_update().get(pk = receiver.pk)
        except Wallet.DoesNotExist:
            raise Exception("receiver wallet does not exist")
    sender_wallet = Wallet.objects.select_for_update().get(pk=sender.pk)

    sender_wallet.balance = sender.balance - amount
    receiver_wallet.balance = receiver.balance + amount


    tx = Transaction.objects.create(
        sender = sender,
        receiver = receiver,
        amount = amount,
        transaction_type = 'CREDIT',
        transaction_status = 'SUCCESS',
        description = description,
        idempotent_key = idempotent_key
    )
    Ledger.objects.create(
        transaction = tx,
        amount = amount,
        wallet = receiver_wallet.balance,
        balance_after = receiver_wallet.balance,
        transaction_type = 'CREDIT',
    )

    Ledger.objects.create(
        transaction=tx,
        amount=amount,
        wallet=sender_wallet.balance,
        balance_after=sender_wallet.balance,
        transaction_type='DEBIT',
    )


    return tx