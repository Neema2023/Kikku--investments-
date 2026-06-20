from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from django.conf import settings

from investments.forms import DepositForm
from investments.models import Deposit
from investments.plans import get_all_vip_plans, get_plan_by_name
from transactions.models import Transaction

from .decorators import active_user_required
from .forms import WithdrawForm


@login_required
@active_user_required
def dashboard_view(request):
    recent_transactions = Transaction.objects.filter(
        user=request.user
    )[:5]

    return render(
        request,
        "dashboard/index.html",
        {
            "recent_transactions": recent_transactions,
        },
    )


@login_required
@active_user_required
def deposit_view(request):
    all_vip_plans = get_all_vip_plans()

    if request.method == "POST":
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
                "Deposit request submitted. Awaiting admin verification."
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
        },
    )


@login_required
@active_user_required
def withdraw_view(request):

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
                "Withdrawal request submitted."
            )
            return redirect("dashboard")

    else:
        form = WithdrawForm(request.user)

    return render(
        request,
        "dashboard/withdraw.html",
        {
            "form": form,
        },
    )


@login_required
@active_user_required
def referrals_view(request):
    referral_link = request.build_absolute_uri(
        reverse("register")
    ) + "?ref=" + request.user.referral_code

    return render(
        request,
        "dashboard/referrals.html",
        {
            "referral_link": referral_link,
            "referral_commission": settings.REFERRAL_COMMISSION_PERCENT,
        },
    )


@login_required
@active_user_required
def profile_view(request):
    return render(
        request,
        "dashboard/profile.html",
    )
