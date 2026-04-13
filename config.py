import os

class Config:

    SBER_API = os.getenv("SBER_API")

    CLIENT_ID = os.getenv("SBER_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SBER_CLIENT_SECRET")

    CERT_PATH = os.getenv("SBER_CERT")
    KEY_PATH = os.getenv("SBER_KEY")

    ACCOUNT_ID = os.getenv("SBER_ACCOUNT")

    REDIS_URL = os.getenv("REDIS_URL")

    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")
