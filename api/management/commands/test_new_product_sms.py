from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Product
from api.MeoService import MeoScraper
from api.sms_service import NotificationService

class Command(BaseCommand):
    help = 'Tests new product detection and notification sending'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Clean up the test product after running the test',
        )

    def handle(self, *args, **options):
        self.stdout.write('Testing new product detection and notification...')
        
        test_product = Product.objects.first()
        
        if test_product:
            message = self.create_product_message(test_product)
            
            notifier = NotificationService()

            notifier.validate_pushover_user()

            success, result = notifier.send_pushover(
                message=message,
                title="New Product Alert",
                url=test_product.url,
                priority=1,
                sound="pushover"
            )

            if success:
                self.stdout.write(self.style.SUCCESS("Pushover notification sent successfully!"))
                self.stdout.write(f"Notification details: {result}")
            else:
                self.stdout.write(self.style.ERROR("Failed to send Pushover notification."))

            # phone_number = "+351932870047"
            # success, result = notifier.send_sms(phone_number, message)
            # if success:
            #     self.stdout.write(self.style.SUCCESS("SMS sent successfully!"))
            # else:
            #     self.stdout.write(self.style.ERROR(f"Failed to send SMS: {result}"))
        else:
            self.stdout.write(self.style.WARNING("No products found in the database."))

        if options['cleanup']:
            self.cleanup_test_product()

    def create_product_message(self, product):
        message = f"{product.name}\n"
        message += f"Points: {product.points}\n"
        message += f"Available: {'Yes' if product.available else 'No'}\n"
        message += f"Stock: {product.stock}\n"
        message += f"Description: {product.description[:100]}...\n"  # Truncate description to 100 characters
        message += f"Last seen: {product.last_seen.strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += f"URL: {product.url}"
        return message

    def cleanup_test_product(self):
        test_product = MeoScraper.get_test_product()
        deleted, _ = Product.objects.filter(name=test_product['name']).delete()
        if deleted:
            self.stdout.write(self.style.SUCCESS('Test product cleaned up'))
        else:
            self.stdout.write(self.style.WARNING('No test product found to clean up'))