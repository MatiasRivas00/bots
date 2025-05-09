from fastapi import FastAPI, Request, HTTPException
import uvicorn
import telegram # Asegúrate de tener instalada la librería python-telegram-bot

# --- Configuración de los Bots ---
BOT_TOKEN_1 = "TU_TOKEN_DEL_BOT_1"
BOT_TOKEN_2 = "TU_TOKEN_DEL_BOT_2"

# Idealmente, la URL base de tu servidor donde FastAPI estará corriendo
WEBHOOK_URL_BASE = "https://tu_dominio_o_ip.com" # Reemplaza con tu URL pública

app = FastAPI()

# --- Lógica para el Bot 1 ---
async def handle_update_bot1(update_data: dict):
    # Aquí procesas la actualización para el bot 1
    # Puedes usar la librería python-telegram-bot o manejarlo directamente
    message = telegram.Update.de_json(update_data, None).message # Ejemplo si usas python-telegram-bot
    if message and message.text:
        print(f"Bot 1 recibió: {message.text}")
        # Aquí iría la lógica para responder con el bot 1
        # bot1.send_message(chat_id=message.chat_id, text=f"Bot 1 dice: {message.text}") # Ejemplo

@app.post(f"/webhook/{BOT_TOKEN_1}") # Usar el token en la ruta es una forma de asegurar la llamada
async def webhook_bot1(request: Request):
    try:
        data = await request.json()
        await handle_update_bot1(data)
        return {"status": "ok"}
    except Exception as e:
        print(f"Error en webhook_bot1: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la actualización del bot 1")

# --- Lógica para el Bot 2 ---
async def handle_update_bot2(update_data: dict):
    # Aquí procesas la actualización para el bot 2
    message = telegram.Update.de_json(update_data, None).message # Ejemplo si usas python-telegram-bot
    if message and message.text:
        print(f"Bot 2 recibió: {message.text}")
        # Aquí iría la lógica para responder con el bot 2
        # bot2.send_message(chat_id=message.chat_id, text=f"Bot 2 dice: {message.text}") # Ejemplo

@app.post(f"/webhook/{BOT_TOKEN_2}") # Ruta diferente para el bot 2
async def webhook_bot2(request: Request):
    try:
        data = await request.json()
        await handle_update_bot2(data)
        return {"status": "ok"}
    except Exception as e:
        print(f"Error en webhook_bot2: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la actualización del bot 2")

# --- Configuración Inicial de Webhooks (ejecutar una vez) ---
async def set_webhooks():
    # (Opcional pero recomendado) Inicializa instancias de bot si usas una librería
    # from telegram.ext import Application
    # application_bot1 = Application.builder().token(BOT_TOKEN_1).build()
    # application_bot2 = Application.builder().token(BOT_TOKEN_2).build()

    # Configurar webhook para Bot 1
    # (Esto asume que tienes una instancia de bot de la librería python-telegram-bot)
    # Ejemplo con la librería python-telegram-bot v20+
    # bot1 = telegram.Bot(token=BOT_TOKEN_1)
    # await bot1.set_webhook(url=f"{WEBHOOK_URL_BASE}/webhook/{BOT_TOKEN_1}")
    # print(f"Webhook para Bot 1 configurado en: {WEBHOOK_URL_BASE}/webhook/{BOT_TOKEN_1}")

    # Configurar webhook para Bot 2
    # bot2 = telegram.Bot(token=BOT_TOKEN_2)
    # await bot2.set_webhook(url=f"{WEBHOOK_URL_BASE}/webhook/{BOT_TOKEN_2}")
    # print(f"Webhook para Bot 2 configurado en: {WEBHOOK_URL_BASE}/webhook/{BOT_TOKEN_2}")

    # --- Alternativa para configurar webhooks usando una petición HTTP GET (más simple) ---
    # Necesitarás hacer esto manualmente una vez o crear una ruta para ello.
    # Ejemplo con curl o un navegador:
    # https://api.telegram.org/bot<BOT_TOKEN_1>/setWebhook?url=<WEBHOOK_URL_BASE>/webhook/<BOT_TOKEN_1>
    # https://api.telegram.org/bot<BOT_TOKEN_2>/setWebhook?url=<WEBHOOK_URL_BASE>/webhook/<BOT_TOKEN_2>
    print("Recuerda configurar los webhooks manualmente o a través de un script.")
    print(f"URL para Bot 1: https://api.telegram.org/bot{BOT_TOKEN_1}/setWebhook?url={WEBHOOK_URL_BASE}/webhook/{BOT_TOKEN_1}")
    print(f"URL para Bot 2: https://api.telegram.org/bot{BOT_TOKEN_2}/setWebhook?url={WEBHOOK_URL_BASE}/webhook/{BOT_TOKEN_2}")


@app.on_event("startup")
async def on_startup():
    # Esta función se ejecuta cuando FastAPI inicia.
    # Es un buen lugar para configurar los webhooks si no lo has hecho manualmente.
    # Ten cuidado de no llamarlo repetidamente sin necesidad.
    # Idealmente, se configura una vez. Puedes comentarlo después de la primera ejecución exitosa.
    # await set_webhooks() # Descomenta si quieres intentar configurar los webhooks al inicio
    print("FastAPI iniciado. Asegúrate de que los webhooks estén configurados.")
    print(f"Endpoint para Bot 1 escuchando en: /webhook/{BOT_TOKEN_1}")
    print(f"Endpoint para Bot 2 escuchando en: /webhook/{BOT_TOKEN_2}")


if __name__ == "__main__":
    # Para desarrollo, puedes ejecutarlo así:
    # uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    # Necesitarás una herramienta como ngrok para exponer tu localhost a internet durante el desarrollo
    # para que Telegram pueda enviar actualizaciones a tu webhook.
    # Ejemplo ngrok: ngrok http 8000
    # Esto te dará una URL https pública que puedes usar como WEBHOOK_URL_BASE.
    uvicorn.run(app, host="0.0.0.0", port=8000)