from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("blocked", "Blocked"),
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    referral_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )

    referred_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_referrals = models.IntegerField(default=0)

    referral_earnings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    vip_plan = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    total_deposits = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_withdrawals = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):

        if not self.referral_code:

            self.referral_code = str(
                random.randint(
                    10000,
                    99999
                )
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
