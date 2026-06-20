from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = [
        "username",
        "phone_number",
        "role",
        "status",
        "balance",
        "vip_plan",
        "total_deposits",
        "total_referrals",
        "referral_earnings",
    ]

    search_fields = [
        "username",
        "phone_number",
        "referral_code",
    ]

    list_filter = [
        "role",
        "status",
    ]
