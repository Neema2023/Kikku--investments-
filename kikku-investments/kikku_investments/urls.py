from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import render

from investments.plans import (
    FEATURED_VIP_PLANS,
    VIP_PLANS,
    HOW_IT_WORKS,
)


def home(request):
    return render(
        request,
        "home.html",
        {
            "featured_vip_plans": FEATURED_VIP_PLANS,
            "vip_plans": VIP_PLANS,
            "how_it_works": HOW_IT_WORKS,
        },
    )


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        home,
        name="home"
    ),

    path(
        "",
        include(
            "accounts.urls"
        )
    ),

    path(
        "",
        include(
            "dashboard.urls"
        )
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
