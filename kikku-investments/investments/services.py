from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from investments.models import UserInvestment
from investments.plans import get_investment_duration, get_plan_by_name
from transactions.models import Transaction


REFERRAL_RATE = Decimal(
    str(settings.REFERRAL_COMMISSION_PERCENT)
) / Decimal("100")


def complete_active_investment(user):
    active = UserInvestment.objects.filter(
        user=user,
        status="active",
    ).first()

    if active:
        active.status = "completed"
        active.completed_at = timezone.now()
        active.save()

    user.vip_plan = None
    user.save(update_fields=["vip_plan"])


@transaction.atomic
def approve_deposit(deposit):
    if deposit.status != "pending":
        return False

    user = deposit.user
    plan = get_plan_by_name(deposit.vip_plan)

    if not plan:
        return False

    complete_active_investment(user)

    total_days = get_investment_duration(deposit.vip_plan)

    UserInvestment.objects.create(
        user=user,
        deposit=deposit,
        vip_plan=deposit.vip_plan,
        amount=deposit.amount,
        daily_reward=plan["daily_reward"],
        total_days=total_days,
        status="active",
    )

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


@transaction.atomic
def process_daily_earnings(for_date=None):
    if for_date is None:
        for_date = timezone.localdate()

    paid_count = 0
    completed_count = 0

    for investment in UserInvestment.objects.filter(status="active"):
        if investment.days_paid >= investment.total_days:
            investment.status = "completed"
            investment.completed_at = timezone.now()
            investment.save()
            complete_active_investment(investment.user)
            completed_count += 1
            continue

        if investment.last_earning_date == for_date:
            continue

        user = investment.user
        user.balance += investment.daily_reward
        user.save(update_fields=["balance"])

        investment.days_paid += 1
        investment.last_earning_date = for_date
        investment.save()

        Transaction.objects.create(
            user=user,
            type="earning",
            amount=investment.daily_reward,
            status="completed",
        )

        paid_count += 1

        if investment.days_paid >= investment.total_days:
            investment.status = "completed"
            investment.completed_at = timezone.now()
            investment.save()
            complete_active_investment(user)
            completed_count += 1

    return paid_count, completed_count
