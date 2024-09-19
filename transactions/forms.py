from django import forms
from .models import Transaction
from accounts.models import UserBankAccount
from django.contrib import messages

BANKRUPT = False


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "transaction_type", "receiver_account"]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account")
        super().__init__(*args, **kwargs)
        self.fields["transaction_type"].disabled = True
        self.fields["transaction_type"].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):  # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get(
            "amount"
        )  # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f"You need to deposit at least {min_deposit_amount} $"
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance  # 1000
        amount = self.cleaned_data.get("amount")

        if BANKRUPT:
            raise forms.ValidationError(
                f"You can not withdraw money. Bank is Bankrupt."
            )
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f"You can withdraw at least {min_withdraw_amount} $"
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f"You can withdraw at most {max_withdraw_amount} $"
            )

        if amount > balance:  # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f"You have {balance} $ in your account. "
                "You can not withdraw more than your account balance"
            )

        return amount


class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        return amount


# class TransferMoneyForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ["receiver_account", "transaction_type", "amount"]

#     def __init__(self, *args, **kwargs):
#         self.account = kwargs.pop("account")
#         super().__init__(*args, **kwargs)
#         self.fields["transaction_type"].disabled = True
#         self.fields["transaction_type"].widget = forms.HiddenInput()

#     def save(self, commit=True):
#         self.instance.account = self.account
#         self.instance.balance_after_transaction = self.account.balance
#         return super().save()

#     def clean_receiver_account(self):
#         receiver_account = self.cleaned_data.get("receiver_account")
#         try:
#             reciever = UserBankAccount.objects.get(account_no=receiver_account)
#         except UserBankAccount.DoesNotExist:
#             raise forms.ValidationError("This user does not exist.")
#         return receiver_account

#     def clean_amount(self):
#         account = self.account
#         balance = account.balance
#         amount = self.cleaned_data.get("amount")

#         if amount > balance:
#             raise forms.ValidationError(
#                 f"You have {balance} $ in your account. "
#                 "You can not transfer more than your account balance"
#             )
#         return amount


class TransferMoneyForm(TransactionForm):
    receiver_account = forms.IntegerField()

    def clean_receiver_account(self):
        receiver_account = self.cleaned_data.get("receiver_account")
        try:
            reciever = UserBankAccount.objects.get(account_no=receiver_account)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError("This user does not exist.")
        return receiver_account

    def clean_amount(self):
        account = self.account
        balance = account.balance
        amount = self.cleaned_data.get("amount")

        if amount > balance:
            raise forms.ValidationError(
                f"You have {balance} $ in your account. "
                "You can not transfer more than your account balance"
            )
        return amount
