from decimal import Decimal
from uuid import UUID

from django.dispatch import receiver

from wallet.models import Wallet, Transaction, Ledger
from django.db import transaction

def deposit(wallet: Wallet, amount: Decimal, idempotent_key: UUID):
    existing_tx = Transaction.objects.filter(idempotent_key = idempotent_key).first()
    if existing_tx:
        return existing_tx
    with transaction.atomic():
         wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
         wallet.balance += amount
         wallet.save(update_fields=['balance'])
         tx = Transaction.objects.create(
            amount=amount,
            transaction_type='CREDIT',
            status='SUCCESS',
            idempotent_key=idempotent_key,
            sender=wallet,
            receiver=wallet

         )
         Ledger.objects.create(
             transaction=tx,
             amount=amount,
             wallet=wallet,
             balance_after=wallet.balance,
             entry_type='CREDIT',
         )
         return tx




