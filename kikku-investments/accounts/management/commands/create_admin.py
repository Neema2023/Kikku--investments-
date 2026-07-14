from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **kwargs):

        phone_number = "0796166472"
        password = "bbb123"

        # username = phone number because login uses phone number
        username = phone_number

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Admin already exists"
                )
            )
            return

        user = CustomUser.objects.create_user(
            username=username,
            phone_number=phone_number,
            password=password,
            first_name="Mukahirwa Thacianne",
            email="admin@classic-investments.com",
            role="admin",
            is_staff=True,
            is_superuser=True,
            status="active",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin created successfully: {user.username}"
            )
        )