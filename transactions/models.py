from accounts.models import UserBankAccount
from django.db import models

# Create your models here.
from .constants import TRANSACTION_TYPE


class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount, related_name="transactions", on_delete=models.CASCADE
    )

    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)
    receiver_account = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["timestamp"]
