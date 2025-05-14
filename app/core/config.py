from app.bot_red.bot import BotRed
from app.core.constants import BOT_RED_TOKEN, ENV
from app.db.mongo import Mongo

BOTS = [
  BotRed(name='red', token=BOT_RED_TOKEN)
]

MONGO_CLIENT = Mongo().connect()
MONGO_MONEY_DB = MONGO_CLIENT['test_money'] if ENV == 'TEST' else MONGO_CLIENT['money'] 