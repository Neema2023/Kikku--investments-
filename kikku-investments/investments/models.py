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


class UserInvestment(models.Model):

    STATUS = [
        ("active", "Active"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investments",
    )

    deposit = models.ForeignKey(
        Deposit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    vip_plan = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    daily_reward = models.DecimalField(max_digits=12, decimal_places=2)
    total_days = models.IntegerField()
    days_paid = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="active",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_earning_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    @property
    def days_remaining(self):
        return max(0, self.total_days - self.days_paid)

    @property
    def total_expected_earnings(self):
        return self.daily_reward * self.total_days

    def __str__(self):
        return f"{self.user.username} - {self.vip_plan} ({self.status})"
