from decimal import Decimal

from django import forms


class WithdrawForm(forms.Form):

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("1"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter amount in FRW",
        }),
        label="Amount",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount > self.user.balance:
            raise forms.ValidationError(
                "Amount exceeds your available balance."
            )
        return amount
