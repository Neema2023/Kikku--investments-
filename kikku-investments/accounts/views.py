from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import CustomUser
from .utils import get_default_referrer


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    referral_code = request.GET.get("ref")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            ref_input = form.cleaned_data.get(
                "referral_code_input"
            )

            referrer = None

            if ref_input:
                try:
                    referrer = CustomUser.objects.get(
                        referral_code=ref_input
                    )
                except CustomUser.DoesNotExist:
                    messages.error(
                        request,
                        "Invalid referral code."
                    )
                    return redirect("register")
            else:
                referrer = get_default_referrer()

            user = form.save(commit=False)

            user.username = form.cleaned_data[
                "phone_number"
            ]

            user.first_name = form.cleaned_data[
                "full_name"
            ]

            user.phone_number = form.cleaned_data[
                "phone_number"
            ]

            if referrer:
                user.referred_by = referrer

            user.save()

            if referrer:
                referrer.total_referrals += 1
                referrer.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect("dashboard")

    else:

        form = RegisterForm(
            initial={
                "referral_code_input":
                referral_code
            }
        )

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        phone = request.POST.get(
            "phone_number"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=phone,
            password=password
        )

        if user:

            if user.status == "blocked":
                messages.error(
                    request,
                    "Your account has been blocked."
                )
                return render(
                    request,
                    "accounts/login.html"
                )

            login(request, user)

            # Redirect admin users to admin panel
            if user.is_superuser or user.role == "admin":
                return redirect("admin_panel")

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid credentials"
        )

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
@staff_member_required
def admin_panel_view(request):
    """Admin panel view - only accessible to superusers and staff"""
    
    # Try to get stats, handle if models don't exist yet
    try:
        from investments.models import Investment
        from payments.models import Deposit
        from transactions.models import Withdrawal
        
        stats = {
            'total_users': CustomUser.objects.count(),
            'active_investments': Investment.objects.filter(status='active').count(),
            'pending_deposits': Deposit.objects.filter(status='pending').count(),
            'pending_withdrawals': Withdrawal.objects.filter(status='pending').count(),
        }
        
        pending_deposits = Deposit.objects.filter(status='pending')[:10]
        pending_withdrawals = Withdrawal.objects.filter(status='pending')[:10]
        
    except (ImportError, AttributeError) as e:
        # If models don't exist yet, show empty stats
        stats = {
            'total_users': CustomUser.objects.count(),
            'active_investments': 0,
            'pending_deposits': 0,
            'pending_withdrawals': 0,
        }
        pending_deposits = []
        pending_withdrawals = []
    
    context = {
        'stats': stats,
        'pending_deposits': pending_deposits,
        'pending_withdrawals': pending_withdrawals,
    }
    return render(request, 'dashboard/admin_panel.html', context)