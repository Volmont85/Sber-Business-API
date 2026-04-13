from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

from config import Config
from sber_client import SberClient
from storage import Storage
from overnight_service import run


cfg = Config()

sber = SberClient(
    cfg.SBER_API,
    cfg.CLIENT_ID,
    cfg.CLIENT_SECRET,
    cfg.CERT_PATH,
    cfg.KEY_PATH
)

storage = Storage(cfg.REDIS_URL)

scheduler = BlockingScheduler(
    timezone=pytz.timezone("Europe/Moscow")
)


@scheduler.scheduled_job(
    "cron",
    day_of_week="mon-fri",
    hour=17,
    minute=0
)
def job():

    run(cfg, sber, storage)


scheduler.start()
