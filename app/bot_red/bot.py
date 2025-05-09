from app.core.utils import BaseBot
from telegram.ext import CommandHandler
from . import handlers

class BotRed(BaseBot):
  def _include_handlers(self):
    self.app.add_handler(CommandHandler("prediction", handlers.prediction))
    self.app.add_handler(CommandHandler("p", handlers.prediction))

    self.app.add_handler(CommandHandler("stop_prediction", handlers.stop_prediction))
    self.app.add_handler(CommandHandler("s", handlers.stop_prediction))

    self.app.add_handler(CommandHandler("default_code", handlers.default_code))
    self.app.add_handler(CommandHandler("dc", handlers.default_code))

    self.app.add_handler(CommandHandler("default_interval", handlers.default_interval))
    self.app.add_handler(CommandHandler("di", handlers.default_interval))

    self.app.add_handler(CommandHandler("default_duration", handlers.default_duration))
    self.app.add_handler(CommandHandler("dd", handlers.default_duration))

    self.app.add_handler(CommandHandler("info", handlers.info))
    self.app.add_handler(CommandHandler("i", handlers.info))