from django.db import models
from django.conf import settings


class Deposit(models.Model):

    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(
        max_length=20
    )

    vip_plan = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    proof_image = models.ImageField(
        upload_to="deposit_proofs/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    referral_paid = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
