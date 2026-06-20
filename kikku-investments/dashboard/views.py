from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse

from django.conf import settings

from accounts.models import CustomUser
from investments.forms import DepositForm
from investments.models import Deposit, UserInvestment
from investments.plans import get_all_vip_plans, get_plan_by_name
from transactions.models import Transaction

from .decorators import active_user_required, admin_user_required
from .forms import WithdrawForm
from .utils import get_available_balance


@login_required
@active_user_required
def dashboard_view(request):
    active_investment = UserInvestment.objects.filter(
        user=request.user,
        status="active",
    ).first()

    recent_transactions = Transaction.objects.filter(
        user=request.user
    )[:10]

    return render(
        request,
        "dashboard/index.html",
        {
            "active_investment": active_investment,
            "recent_transactions": recent_transactions,
            "available_balance": get_available_balance(request.user),
        },
    )


@login_required
@active_user_required
def deposit_view(request):
    all_vip_plans = get_all_vip_plans()
    active_investment = UserInvestment.objects.filter(
        user=request.user,
        status="active",
    ).exists()

    if request.method == "POST":
        if active_investment:
            messages.error(
                request,
                "You already have an active plan. "
                "Wait until it completes before recharging."
            )
            return redirect("dashboard")

        form = DepositForm(request.POST, request.FILES)

        if form.is_valid():
            plan = get_plan_by_name(
                form.cleaned_data["vip_plan"]
            )

            Deposit.objects.create(
                user=request.user,
                phone_number=request.user.phone_number,
                vip_plan=plan["name"],
                amount=plan["amount"],
                proof_image=form.cleaned_data["proof_image"],
            )

            messages.success(
                request,
                "Deposit submitted. Admin will verify your MTN MoMo payment."
            )
            return redirect("dashboard")

    else:
        form = DepositForm()

    return render(
        request,
        "dashboard/deposit.html",
        {
            "form": form,
            "all_vip_plans": all_vip_plans,
            "momo_number": settings.MOMO_NUMBER,
            "has_active_investment": active_investment,
        },
    )


@login_required
@active_user_required
def withdraw_view(request):
    available = get_available_balance(request.user)

    if request.method == "POST":
        form = WithdrawForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            Transaction.objects.create(
                user=request.user,
                type="withdrawal",
                amount=form.cleaned_data["amount"],
                status="pending",
            )

            messages.success(
                request,
                "Withdrawal request submitted. "
                "Admin will send payment to your phone."
            )
            return redirect("dashboard")

    else:
        form = WithdrawForm(request.user)

    return render(
        request,
        "dashboard/withdraw.html",
        {
            "form": form,
            "available_balance": available,
        },
    )


@login_required
@active_user_required
def referrals_view(request):
    referral_link = request.build_absolute_uri(
        reverse("register")
    ) + "?ref=" + request.user.referral_code

    referred_users = CustomUser.objects.filter(
        referred_by=request.user
    ).order_by("-date_joined")

    return render(
        request,
        "dashboard/referrals.html",
        {
            "referral_link": referral_link,
            "referral_commission": settings.REFERRAL_COMMISSION_PERCENT,
            "referred_users": referred_users,
        },
    )


@login_required
@active_user_required
def profile_view(request):
    pending_deposits = Deposit.objects.filter(
        user=request.user,
        status="pending",
    ).count()

    return render(
        request,
        "dashboard/profile.html",
        {
            "pending_deposits": pending_deposits,
        },
    )


@login_required
@admin_user_required
def admin_panel_view(request):
    pending_deposits = Deposit.objects.filter(
        status="pending"
    ).select_related("user")[:20]

    pending_withdrawals = Transaction.objects.filter(
        type="withdrawal",
        status="pending",
    ).select_related("user")[:20]

    stats = {
        "total_users": CustomUser.objects.count(),
        "active_investments": UserInvestment.objects.filter(
            status="active"
        ).count(),
        "pending_deposits": Deposit.objects.filter(
            status="pending"
        ).count(),
        "pending_withdrawals": Transaction.objects.filter(
            type="withdrawal",
            status="pending",
        ).count(),
        "total_deposits": CustomUser.objects.aggregate(
            total=Sum("total_deposits")
        )["total"] or 0,
    }

    return render(
        request,
        "dashboard/admin_panel.html",
        {
            "stats": stats,
            "pending_deposits": pending_deposits,
            "pending_withdrawals": pending_withdrawals,
        },
    )
