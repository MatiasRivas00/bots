from fastapi import APIRouter, Request
from app.core.config import BOTS

router = APIRouter(prefix='/webhook')

for bot in BOTS:
    async def webhook_handler(request: Request):        
        data = await request.json()
        await bot.process_update(data)
        return {"status": "ok"}
    
    router.add_api_route(
        f"/{bot.name}",
        webhook_handler,
        methods=["POST"]
    )