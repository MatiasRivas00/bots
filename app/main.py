from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.core.bots import BOTS
from app.core.constants import PORT
from app.webhooks.router import router as webhook_router
from app.core.logger import logger

async def on_startup():
    logger.info("Iniciando aplicación FastAPI...")
    for bot in BOTS:
        bot.build()
        await bot.init()
        await bot.set_webhook()
        await bot.start()

async def on_shutdown():
    logger.info("Apagando aplicación FastAPI...")
    for bot in BOTS:
        await bot.shutdown()

    logger.info("Aplicación FastAPI apagada.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()

app = FastAPI(title="Multi-Bot FastAPI Service", version="1.0.0", lifespan=lifespan)

app.include_router(webhook_router)


@app.get("/")
async def root():
    return {"message": "Servicio de Bots de Telegram activo. Visita /docs para la documentación de la API."}

if __name__ == "__main__":
    # Para desarrollo, puedes ejecutarlo así:
    # uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    # (Asegúrate que WEBHOOK_URL_BASE en .env o config.py apunte a tu ngrok/IP pública)
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=PORT,
        reload=True # Para desarrollo
    )