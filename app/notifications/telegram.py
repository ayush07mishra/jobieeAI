# 8950241286:AAGcDD05v1RHhE54G_AIU3ygcst3Zr9_27s
# 6968478373

import os
import requests
from dotenv import load_dotenv


load_dotenv()


class TelegramNotifier:

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is missing")

        if not self.chat_id:
            raise ValueError("TELEGRAM_CHAT_ID is missing")

        self.url = (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}/sendMessage"
        )

    def send_message(self, message):

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        return response.json()