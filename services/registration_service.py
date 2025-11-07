from sqlalchemy.orm import Session
from typing import List
from database.repository import RegistrationRepository
from database.models import User, Event, EventRegistration, Platform, RegistrationStatus
from loguru import logger


class RegistrationService:
    @staticmethod
    def register_user_for_event(db: Session, user: User, event: Event, platform: Platform) -> EventRegistration:
        existing = RegistrationRepository.get_by_user_and_event(db, user.id, event.id)
        if existing:
            logger.warning(f"User {user.id} already registered for event {event.id}")
            raise ValueError("Вы уже зарегистрированы на это событие")
        
        confirmed_count = len([r for r in event.registrations if r.status == RegistrationStatus.CONFIRMED.value])
        if confirmed_count >= event.max_participants:
            logger.warning(f"Event {event.id} is full")
            raise ValueError("К сожалению, все места заняты")
        
        registration = RegistrationRepository.create(db, user.id, event.id, platform)
        logger.info(f"User {user.id} registered for event {event.id} via {platform.value}")
        return registration
    
    @staticmethod
    def get_user_registrations(db: Session, user: User) -> List[EventRegistration]:
        return RegistrationRepository.get_user_registrations(db, user.id)
    
    @staticmethod
    def get_event_participants(db: Session, event: Event) -> List[EventRegistration]:
        return RegistrationRepository.get_confirmed_by_event(db, event.id)
