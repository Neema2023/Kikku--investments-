from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):

    help = "Create admin user"

    def handle(self, *args, **kwargs):

        username = "admin"
        phone_number = "0780000000"
        password = "Admin@12345"

        if CustomUser.objects.filter(username=username).exists():
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
            email="admin@classic-investments.com",
            role="admin",
            is_staff=True,
            is_superuser=True,
            status="active"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin created successfully: {user.username}"
            )
        )