from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import BOTS, PORT
from app.webhooks.router import router as webhook_router


app = FastAPI(title="Multi-Bot FastAPI Service", version="1.0.0")

app.include_router(webhook_router)

async def on_startup():
    print("Iniciando aplicación FastAPI...")
    for bot in BOTS:
        await bot.build()
        await bot.set_webhook()

async def on_shutdown():
    print("Apagando aplicación FastAPI...")
    for bot in BOTS:
        await bot.shutdown()

    print("Aplicación FastAPI apagada.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()

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