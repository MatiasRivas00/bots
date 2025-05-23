from abc import ABC, abstractmethod
from telegram.ext import Application
from telegram import Update

from app.core.constants import NGROK_URL
from .logger import logger

class BaseBot(ABC):
  _instances = {}

  def __init__(self, name: str, token: str):
    if self.name != name or self.token != token:
      raise ValueError(
          f"Singleton '{type(self).__name__}' already initialized with "
          f"name='{self.name}' and token='{self.token}'. "
          f"Cannot retrieve it with different values (name='{name}', token='{token}')."
      )

  def __new__(cls, name: str, token: str):
    if cls not in cls._instances:
      instance = super().__new__(cls)
      instance.name = name
      instance.token = token
      instance._built = False
      instance.app = None
      cls._instances[cls] = instance

    return cls._instances[cls]
  
  @abstractmethod
  def _include_handlers(self):
    # the only way to call this method is trough build
    # so you can assume that self.app already exists to add handlers
    pass
  
  def build(self):
    if hasattr(self, '_built') and self._built:
      return self

    self.app = Application.builder().token(self.token).build()
    self._include_handlers()
    self._built = True
    return self
  
  async def init(self):
    if hasattr(self, '_built') and self._built:
      await self.app.initialize()

  async def start(self):
    if hasattr(self, '_built') and self._built:
      await self.app.start()

  async def init(self):
    if hasattr(self, '_built') and self._built:
      await self.app.initialize()

  async def set_webhook(self):
    if hasattr(self, 'app'):
      url = f"{NGROK_URL}/webhook/{self.name}"
      await self.app.bot.set_webhook(
        url=url,
        allowed_updates=Update.ALL_TYPES
      )
      logger.info(f"Webhook establecido en {url}")
      webhook_info = await self.app.bot.get_webhook_info()
      logger.info(f"Confirmación Webhook: {webhook_info}")
  
  async def shutdown(self):
    if hasattr(self, 'app') and self.app:
      try:
        logger.info(f"stopping bot {self.name}")
        await self.app.stop()
      except Exception as e:
        logger.error(f"stopping bot {self.name} failed, reason {e}", exc_info=True)

      try:
        logger.info(f"deleting webhook from bot {self.name}")
        await self.app.bot.delete_webhook()
      except Exception as e:
        logger.error(f"delete webhook from bot {self.name} failed, reason {e}", exc_info=True)
      
      try:
        logger.info(f"shutdown bot {self.name}")
        await self.app.shutdown()
      except Exception as e:
        logger.error(f"shutdown bot {self.name} failed, reason {e}", exc_info=True)

  async def process_update(self, data):
    if not hasattr(self, 'app') or self.app is None:
      print(f"Error: process_update called {self.name} before building app")
      raise RuntimeError(f"Bot application for '{self.name}' is not built")
    
    try:
      update = Update.de_json(data, self.app.bot)
      await self.app.process_update(update)
    except Exception as e:
       print(f"Error processing update handlers for {self.name}: {e}")


  def run_polling(self):
    self.app.run_polling()