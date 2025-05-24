from app.core.utils import BaseBot
from telegram.ext import CommandHandler
from . import handlers

class BotMoney(BaseBot):
  def _include_handlers(self):
    self.app.add_handler(CommandHandler("t", handlers.handle_transaction))
    self.app.add_handler(CommandHandler("transaction", handlers.handle_transaction))

    self.app.add_handler(CommandHandler("week", handlers.handle_week_summary))
    self.app.add_handler(CommandHandler("month", handlers.handle_month_summary))
    self.app.add_handler(CommandHandler("year", handlers.handle_year_summary))
