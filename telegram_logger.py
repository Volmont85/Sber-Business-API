import httpx

class TelegramLogger:

    def __init__(self, token, chat_id):

        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    def send(self, text):

        try:
            httpx.post(
                self.url,
                json={
                    "chat_id": self.chat_id,
                    "text": text
                },
                timeout=10
            )
        except Exception:
            pass
