import uuid

from django.db import models
from django.conf import settings
from wallet.util import generate_account_number, generate_reference


# Create your models here.
class Wallet(models.Model):
    CURRENCY_CHOICES = (
    ("NGN", "Naira"),
    ("USD", "Dollar"),
    ("EUR", "Euro"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="wallet")
    wallet_number = models.CharField(max_length=10, unique=True, primary_key=True)
    account_number = models.CharField(max_length=10, unique=True, default=generate_account_number)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="NGN")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



def __str__(self):
    return f"account number : {self.wallet_number}"


class Transaction(models.Model):
        TRANSACTION_TYPE = (
          ("DEBIT", "Debit"),
          ("CREDIT", "Credit"),
        )

        TRANSACTION_STATUS = (
            ("PENDING", "Pending"),
            ("SUCCESS", "Success"),
            ("FAILED", "Failed"),

        )
        reference = models.CharField(max_length=10, default=generate_reference)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
        sender = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="sender")
        receiver = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="receiver")
        status = models.CharField(max_length=10, choices=TRANSACTION_STATUS)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        idempotent_key = models.UUIDField(default=uuid.uuid4, editable=False)


        def __str__(self):
            return f"sender : {self.sender}, receiver : {self.receiver} "



class Ledger(models.Model):
    ENTRY_TYPE = (
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    )
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name="ledger")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="ledger")
    entry_type = models.CharField(max_length=6, choices=ENTRY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ledger : {self.transaction}"

