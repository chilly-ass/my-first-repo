import os
import asyncio
from aiogram import Bot
from loguru import logger

BOT_TOKEN = os.getenv("BOT_TOKEN")
REPLIT_DOMAINS = os.getenv("REPLIT_DOMAINS")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN not set")
    exit(1)

if not REPLIT_DOMAINS:
    logger.error("REPLIT_DOMAINS not set")
    exit(1)

webhook_url = f"https://{REPLIT_DOMAINS}/telegram"

async def setup():
    bot = Bot(token=BOT_TOKEN)
    
    try:
        await bot.set_webhook(webhook_url, drop_pending_updates=True)
        logger.info(f"✅ Webhook successfully set to: {webhook_url}")
        
        webhook_info = await bot.get_webhook_info()
        logger.info(f"Current webhook: {webhook_info.url}")
        logger.info(f"Pending updates: {webhook_info.pending_update_count}")
        
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(setup())
