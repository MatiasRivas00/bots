from app.core.utils import BaseBot
from telegram.ext import CommandHandler
from . import handlers

class BotMoney(BaseBot):
  def _include_handlers(self):
    self.app.add_handler(CommandHandler("t", handlers.handle_transaction))
    self.app.add_handler(CommandHandler("transaction", handlers.handle_transaction))