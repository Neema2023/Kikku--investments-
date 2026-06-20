from django.conf import settings


def community_links(request):
    return {
        "whatsapp_phone": settings.WHATSAPP_PHONE,
        "whatsapp_contact_url": settings.WHATSAPP_CONTACT_URL,
        "whatsapp_community_url": settings.WHATSAPP_COMMUNITY_URL,
        "telegram_group_url": settings.TELEGRAM_GROUP_URL,
    }
