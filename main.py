import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from loguru import logger
import sys

from config import settings
from database.connection import init_db
from telegram.handlers import router
from services.notification_service import NotificationService
from scheduler.scheduler import setup_scheduler

logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

notification_service = NotificationService(bot)
scheduler = setup_scheduler(notification_service)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    
    init_db()
    logger.info("Database initialized")
    
    webhook_url = settings.WEBHOOK_URL
    if not webhook_url:
        replit_domains = os.getenv("REPLIT_DOMAINS")
        if replit_domains:
            webhook_url = f"https://{replit_domains}"
            logger.info(f"Auto-detected Replit domain: {webhook_url}")
    
    if webhook_url:
        full_webhook_url = f"{webhook_url.rstrip('/')}{settings.WEBHOOK_PATH}"
        await bot.set_webhook(full_webhook_url, drop_pending_updates=True)
        logger.info(f"Webhook set to: {full_webhook_url}")
    else:
        logger.warning("WEBHOOK_URL not set and REPLIT_DOMAINS not available, webhook not configured")
    
    scheduler.start()
    logger.info("Scheduler started")
    
    yield
    
    logger.info("Shutting down...")
    scheduler.shutdown()
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan, title="Event Registration Bot")


@app.post(settings.WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = await request.json()
    from aiogram.types import Update
    await dp.feed_update(bot, Update(**update))
    return {"ok": True}


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "bot_configured": bool(settings.BOT_TOKEN),
        "webhook_configured": bool(settings.WEBHOOK_URL),
        "database_url": "configured" if settings.DATABASE_URL else "not configured"
    }


@app.get("/")
async def root():
    return {
        "app": "Event Registration Bot",
        "status": "running",
        "endpoints": {
            "telegram_webhook": settings.WEBHOOK_PATH,
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
