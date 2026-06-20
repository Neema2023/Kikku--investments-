from django.contrib import admin
from django.contrib import messages

from investments.services import approve_withdrawal, reject_withdrawal

from .models import Transaction


@admin.action(description="Approve selected withdrawals")
def approve_withdrawals(modeladmin, request, queryset):
    approved = 0
    for withdrawal in queryset.filter(
        type="withdrawal",
        status="pending",
    ):
        if approve_withdrawal(withdrawal):
            approved += 1

    messages.success(
        request,
        f"{approved} withdrawal(s) approved."
    )


@admin.action(description="Reject selected withdrawals")
def reject_withdrawals(modeladmin, request, queryset):
    rejected = 0
    for withdrawal in queryset.filter(
        type="withdrawal",
        status="pending",
    ):
        if reject_withdrawal(withdrawal):
            rejected += 1

    messages.success(
        request,
        f"{rejected} withdrawal(s) rejected."
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "type",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("type", "status")
    search_fields = ("user__username",)
    actions = [approve_withdrawals, reject_withdrawals]
