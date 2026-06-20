from django.core.management.base import BaseCommand

from investments.services import process_daily_earnings


class Command(BaseCommand):
    help = "Credit daily VIP earnings to active investors"

    def handle(self, *args, **options):
        paid, completed = process_daily_earnings()
        self.stdout.write(
            self.style.SUCCESS(
                f"Daily earnings processed: {paid} paid, "
                f"{completed} investments completed."
            )
        )
