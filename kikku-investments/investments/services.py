from decimal import Decimal

from django.conf import settings
from django.db import transaction

from transactions.models import Transaction


REFERRAL_RATE = Decimal(
    str(settings.REFERRAL_COMMISSION_PERCENT)
) / Decimal("100")


@transaction.atomic
def approve_deposit(deposit):
    if deposit.status != "pending":
        return False

    user = deposit.user
    user.vip_plan = deposit.vip_plan
    user.total_deposits += deposit.amount
    user.save()

    deposit.status = "approved"
    deposit.save()

    Transaction.objects.create(
        user=user,
        type="deposit",
        amount=deposit.amount,
        status="approved",
    )

    if user.referred_by and not deposit.referral_paid:
        commission = (
            deposit.amount * REFERRAL_RATE
        ).quantize(Decimal("0.01"))

        referrer = user.referred_by
        referrer.balance += commission
        referrer.referral_earnings += commission
        referrer.save()

        deposit.referral_paid = True
        deposit.save()

        Transaction.objects.create(
            user=referrer,
            type="referral",
            amount=commission,
            status="completed",
        )

    return True


@transaction.atomic
def reject_deposit(deposit):
    if deposit.status != "pending":
        return False

    deposit.status = "rejected"
    deposit.save()
    return True


@transaction.atomic
def approve_withdrawal(withdrawal):
    if withdrawal.type != "withdrawal" or withdrawal.status != "pending":
        return False

    user = withdrawal.user
    if user.balance < withdrawal.amount:
        return False

    user.balance -= withdrawal.amount
    user.total_withdrawals += withdrawal.amount
    user.save()

    withdrawal.status = "completed"
    withdrawal.save()
    return True


@transaction.atomic
def reject_withdrawal(withdrawal):
    if withdrawal.type != "withdrawal" or withdrawal.status != "pending":
        return False

    withdrawal.status = "rejected"
    withdrawal.save()
    return True
