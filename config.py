import os

class Config:

    SBER_API = os.getenv("SBER_API")

    CLIENT_ID = os.getenv("SBER_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SBER_CLIENT_SECRET")

    CERT_PATH = os.getenv("SBER_CERT")
    KEY_PATH = os.getenv("SBER_KEY")

    ACCOUNT_ID = os.getenv("SBER_ACCOUNT")

    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    REDIS_URL = os.getenv("REDIS_URL")

    BALANCE_THRESHOLD = 1_300_000
    RESERVE_AMOUNT = 300_000

    MOSCOW_TZ = "Europe/Moscow"

    RUN_HOUR = 18
    RUN_MINUTE = 5

    CUT_OFF_HOUR = 18
    CUT_OFF_MINUTE = 30
