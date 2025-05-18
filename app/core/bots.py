from app.bot_red.bot import BotRed
from app.bot_money.bot import BotMoney

from app.core.constants import BOT_RED_TOKEN, BOT_MONEY_TOKEN

BOTS = [
  BotRed(name='red', token=BOT_RED_TOKEN),
  BotMoney(name='money', token=BOT_MONEY_TOKEN)
]