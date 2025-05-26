from django.utils import timezone
from .models import CartItem
import logging
from apscheduler.schedulers.background import BackgroundScheduler
logger = logging.getLogger(__name__)

def CleaningOfCart():
    logger.info('===== inside the scheduler function ==== ')
    now = timezone.now()
    expired_carts = CartItem.objects.filter(added_at__lt=now - timezone.timedelta(minutes=3))
    logger.info(f'===== carts ==== {expired_carts}')
    count = expired_carts.count()
    logger.info(f'==== carts count ==== {count}')
    expired_carts.delete()
    logger.info(f"{count} expired cart items deleted.")


def start():
    logger.info('====== scheduler strated ====')
    scheduler = BackgroundScheduler()
    scheduler.add_job(CleaningOfCart, 'interval', minutes=2)
    scheduler.start()