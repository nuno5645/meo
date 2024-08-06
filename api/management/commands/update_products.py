from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Product, CronJobLog
from api.MeoService import MeoScraper
from api.sms_service import NotificationService
from prettytable import PrettyTable

class Command(BaseCommand):
    help = 'Updates product data from MEO website, sends notifications for new products, and displays all products'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notifier = NotificationService()

    def handle(self, *args, **options):
        cron_log = CronJobLog(cron_id='update_products')
        cron_log.save()

        try:
            self.stdout.write('Updating products...')
            
            products_data = MeoScraper.scrape_sensacoes_meos()
            self.stdout.write(f'Scraped {len(products_data)} products')
            
            all_products = set(Product.objects.values_list('name', flat=True))
            new_products = []
            
            for product in products_data:
                product_obj, created = self.update_or_create_product(product)
                if created:
                    new_products.append(product_obj)
                    self.stdout.write(f'New product added: {product_obj.name}')
                if product['name'] in all_products:
                    all_products.remove(product['name'])
            
            unavailable_products = Product.objects.filter(name__in=all_products, available=True)
            unavailable_products.update(available=False, stock=0)
            for product in unavailable_products:
                self.stdout.write(f'Product marked as unavailable: {product.name}')
                            
            # Send notifications for new products
            if new_products:
                self.send_new_products_notifications(new_products)
            
            self.stdout.write(self.style.SUCCESS('Successfully updated products'))
            
            # Print summary
            self.stdout.write(f'Total products scraped: {len(products_data)}')
            self.stdout.write(f'New products added: {len(new_products)}')
            self.stdout.write(f'Products marked as unavailable: {len(unavailable_products)}')
            
            # Display table with all products
            self.display_products_table()

            cron_log.status = True
            cron_log.save()

        except Exception as e:
            cron_log.status = False
            cron_log.error_message = str(e)
            cron_log.save()
            
            # Send error notifications
            self.send_error_notifications(str(e))
            
            raise e

    def update_or_create_product(self, product):
        return Product.objects.update_or_create(
            name=product['name'],
            defaults={
                'points': product['points'],
                'url': product['url'],
                'available': product['available'],
                'image_url': product['image_url'],
                'link_url': product['link_url'],
                'description': product['description'],
                'stock': product['stock'],
                'last_seen': timezone.now(),
                'is_new': True if product['name'] not in Product.objects.values_list('name', flat=True) else False
            }
        )

    def send_new_products_notifications(self, new_products):
        for product in new_products:
            message = self.create_product_message(product)
            
            # Send Pushover notification
            success, result = self.notifier.send_pushover(
                message=message,
                title="New MEO Product Available",
                url=product.link_url,
                priority=1,
                sound="pushover"
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS(f"Pushover notification sent for new product: {product.name}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to send Pushover notification for new product: {product.name}. Error: {result}"))

            # Send SMS
            phone_number = "+351932870047"  # Replace with the desired phone number
            success, result = self.notifier.send_sms(phone_number, message)
            if success:
                self.stdout.write(self.style.SUCCESS(f"SMS sent for new product: {product.name}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to send SMS for new product: {product.name}. Error: {result}"))

    def create_product_message(self, product):
        message = f"New MEO product available: {product.name}\n"
        message += f"Points: {product.points}\n"
        message += f"Stock: {product.stock}\n"
        message += f"Description: {product.description[:100]}...\n"  # Truncate description to 100 characters
        message += f"URL: {product.link_url}"
        return message

    def display_products_table(self):
        table = PrettyTable()
        table.field_names = ["Name", "Points", "Available", "Stock", "Last Seen", "Is New"]
        table.align["Name"] = "l"
        table.align["Points"] = "r"
        table.align["Available"] = "c"
        table.align["Stock"] = "r"
        table.align["Last Seen"] = "c"
        table.align["Is New"] = "c"

        new_product_names = set(Product.objects.filter(is_new=True).values_list('name', flat=True))

        for product in Product.objects.all().order_by('name'):
            row = [
                product.name,
                str(product.points),
                "Yes" if product.available else "No",
                str(product.stock),
                product.last_seen.strftime("%Y-%m-%d %H:%M:%S"),
                "Yes" if product.is_new else "No"
            ]
            
            if product.name in new_product_names:
                row = [f"\033[92m{cell}\033[0m" for cell in row]
            
            table.add_row(row)

        self.stdout.write("\nAll Products:")
        self.stdout.write(str(table))

    def send_error_notifications(self, error_message):
        message = f"Error occurred during product update:\n{error_message}"

        # Send Pushover notification
        success, result = self.notifier.send_pushover(
            message=message,
            title="MEO Product Update Error",
            priority=2,
            sound="siren"
        )

        if success:
            self.stdout.write(self.style.SUCCESS("Pushover error notification sent"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to send Pushover error notification. Error: {result}"))

        # Send SMS
        phone_number = "+351932870047"  # Replace with the desired phone number
        success, result = self.notifier.send_sms(phone_number, message)
        if success:
            self.stdout.write(self.style.SUCCESS("SMS error notification sent"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to send SMS error notification. Error: {result}"))