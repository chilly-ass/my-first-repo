from aiogram import Bot
from database.models import Event, EventRegistration
from utils.formatters import format_reminder
from loguru import logger
from typing import List


class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def send_event_reminders(self, event: Event, hours_before: int, registrations: List[EventRegistration]):
        message = format_reminder(event, hours_before)
        
        for registration in registrations:
            user = registration.user
            
            try:
                if user.telegram_id:
                    await self.bot.send_message(
                        chat_id=user.telegram_id,
                        text=message,
                        parse_mode="HTML"
                    )
                    logger.info(f"Sent {hours_before}h reminder to telegram user {user.telegram_id} for event {event.id}")
            except Exception as e:
                logger.error(f"Failed to send reminder to user {user.id}: {e}")
