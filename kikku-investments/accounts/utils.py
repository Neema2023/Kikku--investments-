from .models import CustomUser


def get_default_referrer():
    referrer = CustomUser.objects.filter(role="admin").first()
    if referrer:
        return referrer
    return CustomUser.objects.filter(is_superuser=True).first()
