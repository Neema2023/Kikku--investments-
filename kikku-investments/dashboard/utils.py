from django.db.models import Sum

from transactions.models import Transaction


def get_available_balance(user):
    pending = Transaction.objects.filter(
        user=user,
        type="withdrawal",
        status="pending",
    ).aggregate(total=Sum("amount"))["total"] or 0

    return user.balance - pending
