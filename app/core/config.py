from app.bot_red.bot import BotRed
from app.core.constants import BOT_RED_TOKEN
from app.db.mongo import Mongo

BOTS = [
  BotRed(name='red', token=BOT_RED_TOKEN)
]

MONGO_CLIENT = Mongo().connect()