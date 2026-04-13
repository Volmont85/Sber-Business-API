from datetime import datetime
from telegram_logger import send_message


MIN_BALANCE = 1_300_000
RESERVE = 300_000


def run(cfg, sber, storage):

    if not storage.lock_today():
        return

    token = sber.get_token()

    balance = sber.get_balance(token, cfg.ACCOUNT_ID)

    if balance <= MIN_BALANCE:
        return

    amount = balance - RESERVE

    rate = sber.get_interest_rate(token, amount)

    external_id = "overnight-" + datetime.now().strftime("%Y%m%d")

    result = sber.create_deposit(
        token,
        amount,
        rate,
        external_id
    )

    message = f"""
Overnight создан

Сумма: {amount}
Ставка: {rate}
ID: {external_id}
"""

    send_message(
        cfg.TG_TOKEN,
        cfg.TG_CHAT_ID,
        message
    )
