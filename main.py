import os
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from sber_client import SberClient
from overnight_service import OvernightService
from storage import Storage
from telegram_logger import TelegramLogger

config = Config()

def check_file(path, name):
    if not path or not os.path.exists(path):
        print(f"{name} not found: {path}")
        sys.exit(1)

check_file(config.CERT_PATH, "Client cert")
check_file(config.KEY_PATH, "Client key")
check_file("/app/sber_ca.pem", "CA cert")

sber = SberClient(
    config.SBER_API,
    config.CLIENT_ID,
    config.CLIENT_SECRET,
    config.CERT_PATH,
    config.KEY_PATH
)

print("CERT:", config.CERT_PATH)
print("KEY:", config.KEY_PATH)

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
