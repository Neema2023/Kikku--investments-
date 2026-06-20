from django.urls import path

from .views import (
    dashboard_view,
    deposit_view,
    withdraw_view,
    referrals_view,
    profile_view,
)

urlpatterns = [

    path(
        "dashboard/",
        dashboard_view,
        name="dashboard"
    ),

    path(
        "dashboard/deposit/",
        deposit_view,
        name="deposit"
    ),

    path(
        "dashboard/withdraw/",
        withdraw_view,
        name="withdraw"
    ),

    path(
        "dashboard/referrals/",
        referrals_view,
        name="referrals"
    ),

    path(
        "dashboard/profile/",
        profile_view,
        name="profile"
    ),
]
