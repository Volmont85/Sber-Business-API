import os

import config
print("CLIENT_ID:", config.CLIENT_ID)
print("CLIENT_SECRET:", config.CLIENT_SECRET)


from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from sber_client import SberClient
from overnight_service import OvernightService
from storage import Storage
from telegram_logger import TelegramLogger

config = Config()

sber = SberClient(
    config.SBER_API,
    config.CLIENT_ID,
    config.CLIENT_SECRET,
    config.CERT_PATH,
    config.KEY_PATH
)

storage = Storage(config.REDIS_URL)

logger = TelegramLogger(
    config.TG_TOKEN,
    config.TG_CHAT_ID
)

service = OvernightService(
    config,
    sber,
    storage,
    logger
)

scheduler = BlockingScheduler(
    timezone=config.MOSCOW_TZ
)

scheduler.add_job(
    service.run,
    "cron",
    day_of_week="mon-fri",
    hour=config.RUN_HOUR,
    minute=config.RUN_MINUTE
)

scheduler.start()
