from fastapi import APIRouter, Request
from app.core.bots import BOTS

router = APIRouter(prefix='/webhook')

def create_webhook_handler(bot):
    async def webhook_handler(request: Request):
        data = await request.json()
        await bot.process_update(data)
        return {"status": "ok"}
    return webhook_handler

for bot in BOTS:
    router.add_api_route(
        f"/{bot.name}",
        create_webhook_handler(bot),
        methods=["POST"]
    )