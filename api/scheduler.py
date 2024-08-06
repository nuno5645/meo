from datetime import datetime
from django.core.management import call_command
import logging

def scheduler():
    logging.basicConfig(filename='/src/log/debug_cron.log', level=logging.DEBUG)

    logging.debug("Scheduler function ran at: " + str(datetime.now()))
    # Your scheduler logic here
    print("Scheduler is running")

    call_command('update_products')

if __name__ == "__main__":
    scheduler()