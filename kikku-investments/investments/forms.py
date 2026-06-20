from django import forms

from investments.plans import get_vip_plan_choices


class DepositForm(forms.Form):

    vip_plan = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
        label="Select VIP Plan",
    )

    proof_image = forms.ImageField(
        label="Upload Proof of Payment",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vip_plan"].choices = get_vip_plan_choices()
