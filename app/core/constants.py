from dotenv import load_dotenv
import os

load_dotenv(override=True)

BOT_RED_TOKEN = os.getenv("BOT_RED_TOKEN")
RED_TOKEN_URL = os.getenv("RED_TOKEN_URL")
RED_PREDICTION_URL = os.getenv("RED_PREDICTION_URL")

BOT_MONEY_TOKEN = os.getenv("BOT_MONEY_TOKEN")

PORT = int(os.getenv("PORT"))
NGROK_URL = os.getenv("NGROK_URL")
print(NGROK_URL)

MONGO_URI = os.getenv("MONGO_URI")

ENV = os.getenv("ENV")

GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
