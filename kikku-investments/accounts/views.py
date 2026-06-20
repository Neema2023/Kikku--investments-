from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from .forms import RegisterForm

from .models import CustomUser


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
