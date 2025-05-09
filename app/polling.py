import threading
import asyncio
from app.core.config import BOTS

BOTS[0].build()
BOTS[0].run_polling()