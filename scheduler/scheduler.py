from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from scheduler.tasks import check_and_send_reminders


def setup_scheduler(notification_service) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        check_and_send_reminders,
        trigger=IntervalTrigger(hours=1),
        args=[notification_service, 24],
        id="reminder_24h",
        name="24 hour reminder check",
        replace_existing=True
    )
    
    scheduler.add_job(
        check_and_send_reminders,
        trigger=IntervalTrigger(hours=1),
        args=[notification_service, 1],
        id="reminder_1h",
        name="1 hour reminder check",
        replace_existing=True
    )
    
    logger.info("Scheduler configured with reminder tasks")
    return scheduler
