from dotenv import load_dotenv
import os

load_dotenv()

BOT_RED_TOKEN = os.getenv("BOT_RED_TOKEN")
RED_TOKEN_URL = os.getenv("RED_TOKEN_URL")
RED_PREDICTION_URL = os.getenv("RED_PREDICTION_URL")

BOT_BUDGET_TOKEN = os.getenv("BOT_BUDGET_TOKEN")

PORT = int(os.getenv("PORT"))
NGROK_URL = os.getenv("NGROK_URL")

MONGO_URI = os.getenv("MONGO_URI")