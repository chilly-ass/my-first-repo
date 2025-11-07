from sqlalchemy.orm import Session
from typing import List, Optional
from database.repository import EventRepository
from database.models import Event
from loguru import logger


class EventService:
    @staticmethod
    def get_upcoming_events(db: Session) -> List[Event]:
        events = EventRepository.get_upcoming(db)
        logger.info(f"Found {len(events)} upcoming events")
        return events
    
    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
        return EventRepository.get_by_id(db, event_id)
    
    @staticmethod
    def get_events_for_reminder(db: Session, hours_before: int) -> List[Event]:
        events = EventRepository.get_events_in_timeframe(db, hours_before)
        logger.info(f"Found {len(events)} events {hours_before}h before start")
        return events
