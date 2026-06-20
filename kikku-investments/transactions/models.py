from django.db import models
from django.conf import settings


class Transaction(models.Model):

    TYPES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("earning", "Earning"),
        ("referral", "Referral"),
    ]

    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=30,
        choices=TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
