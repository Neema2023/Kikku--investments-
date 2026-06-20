from django.contrib import admin
from django.contrib import messages

from .models import Deposit, UserInvestment
from .services import approve_deposit, reject_deposit


@admin.action(description="Approve selected deposits")
def approve_deposits(modeladmin, request, queryset):
    approved = 0
    for deposit in queryset.filter(status="pending"):
        if approve_deposit(deposit):
            approved += 1

    messages.success(
        request,
        f"{approved} deposit(s) approved."
    )


@admin.action(description="Reject selected deposits")
def reject_deposits(modeladmin, request, queryset):
    rejected = 0
    for deposit in queryset.filter(status="pending"):
        if reject_deposit(deposit):
            rejected += 1

    messages.success(
        request,
        f"{rejected} deposit(s) rejected."
    )


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "vip_plan",
        "status",
        "referral_paid",
        "created_at",
    )
    list_filter = ("status", "vip_plan", "referral_paid")
    search_fields = ("user__username", "phone_number")
    actions = [approve_deposits, reject_deposits]
    readonly_fields = ("referral_paid",)


@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "vip_plan",
        "daily_reward",
        "days_paid",
        "total_days",
        "status",
        "started_at",
    )
    list_filter = ("status", "vip_plan")
    search_fields = ("user__username", "user__phone_number")
