from datetime import datetime
import pytz
import time

class OvernightService:

    def __init__(self, config, sber, storage, logger):

        self.config = config
        self.sber = sber
        self.storage = storage
        self.logger = logger

    def run(self):

        tz = pytz.timezone(self.config.MOSCOW_TZ)
        now = datetime.now(tz)

        cut_off = now.replace(
            hour=self.config.CUT_OFF_HOUR,
            minute=self.config.CUT_OFF_MINUTE,
            second=0
        )

        if now > cut_off:
            self.logger.send("❌ Cut‑off passed. Deposit skipped.")
            return

        if self.storage.already_completed():
            self.logger.send("⚠️ Overnight already completed today")
            return

        if not self.storage.acquire_lock():
            self.logger.send("⚠️ Another process is already running")
            return

        try:

            token = self.sber.get_token()

            balance = self.sber.get_balance(
                token,
                self.config.ACCOUNT_ID
            )

            self.logger.send(f"Баланс: {balance:,.0f} ₽")

            if balance <= self.config.BALANCE_THRESHOLD:

                self.logger.send("Баланс ниже порога")
                return

            amount = balance - self.config.RESERVE_AMOUNT

            external_id = self.storage.get_external_id()

            rate = self.sber.get_interest_rate(token, amount)

            if not self.storage.application_created():

                try:

                    self.sber.create_deposit(
                        token,
                        amount,
                        rate,
                        external_id
                    )

                    self.storage.mark_application_created()

                except Exception:

                    self.logger.send("Ставка изменилась. Пробуем получить новую.")

                    rate = self.sber.get_interest_rate(token, amount)

                    self.sber.create_deposit(
                        token,
                        amount,
                        rate,
                        external_id
                    )

                    self.storage.mark_application_created()

            self.logger.send(
                f"Заявка отправлена\n"
                f"Сумма {amount:,.0f}\n"
                f"Ставка {rate}%"
            )

            for _ in range(10):

                state = self.sber.get_application_state(
                    token,
                    external_id
                )

                status = state.get("state")

                if status in ["ACCEPTED", "PLACED"]:

                    self.storage.mark_completed()

                    self.logger.send(
                        f"✅ Overnight размещен\n"
                        f"Статус {status}"
                    )

                    return

                if status in ["REJECTED", "FAILED"]:

                    self.logger.send(
                        f"❌ Банк отклонил заявку\n"
                        f"Статус {status}"
                    )

                    return

                time.sleep(10)

            self.logger.send(
                "⚠️ Не удалось подтвердить статус заявки"
            )

        finally:

            self.storage.release_lock()
