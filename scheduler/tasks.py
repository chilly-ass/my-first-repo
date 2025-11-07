from loguru import logger
from database.connection import get_db
from services.event_service import EventService
from services.registration_service import RegistrationService


async def check_and_send_reminders(notification_service, hours_before: int):
    logger.info(f"Running reminder check for {hours_before}h before events")
    
    try:
        with get_db() as db:
            events = EventService.get_events_for_reminder(db, hours_before)
            
            for event in events:
                registrations = RegistrationService.get_event_participants(db, event)
                
                if registrations:
                    logger.info(f"Sending {hours_before}h reminders for event {event.id} to {len(registrations)} users")
                    await notification_service.send_event_reminders(event, hours_before, registrations)
                    
    except Exception as e:
        logger.error(f"Error in reminder task: {e}")
