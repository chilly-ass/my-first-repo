from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import Optional, List
from database.models import User, Event, EventRegistration, UserState, Platform, RegistrationStatus


class UserRepository:
    @staticmethod
    def get_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
        return db.query(User).filter(User.telegram_id == telegram_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create(db: Session, name: str, email: str, telegram_id: Optional[int] = None, 
               whatsapp_phone: Optional[str] = None) -> User:
        user = User(
            name=name,
            email=email,
            telegram_id=telegram_id,
            whatsapp_phone=whatsapp_phone
        )
        db.add(user)
        db.flush()
        return user
    
    @staticmethod
    def update_telegram_id(db: Session, user: User, telegram_id: int) -> User:
        user.telegram_id = telegram_id
        user.updated_at = datetime.utcnow()
        db.flush()
        return user


class EventRepository:
    @staticmethod
    def get_all(db: Session) -> List[Event]:
        return db.query(Event).order_by(Event.date_time).all()
    
    @staticmethod
    def get_upcoming(db: Session) -> List[Event]:
        return db.query(Event).filter(Event.date_time > datetime.utcnow()).order_by(Event.date_time).all()
    
    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Optional[Event]:
        return db.query(Event).filter(Event.id == event_id).first()
    
    @staticmethod
    def create(db: Session, title: str, description: str, date_time: datetime, 
               location: str, max_participants: int = 50) -> Event:
        event = Event(
            title=title,
            description=description,
            date_time=date_time,
            location=location,
            max_participants=max_participants
        )
        db.add(event)
        db.flush()
        return event
    
    @staticmethod
    def get_events_in_timeframe(db: Session, hours_before: int, tolerance_minutes: int = 30) -> List[Event]:
        target_time = datetime.utcnow() + timedelta(hours=hours_before)
        start_time = target_time - timedelta(minutes=tolerance_minutes)
        end_time = target_time + timedelta(minutes=tolerance_minutes)
        
        return db.query(Event).filter(
            and_(
                Event.date_time >= start_time,
                Event.date_time <= end_time
            )
        ).all()


class RegistrationRepository:
    @staticmethod
    def get_by_user_and_event(db: Session, user_id: int, event_id: int) -> Optional[EventRegistration]:
        return db.query(EventRegistration).filter(
            and_(
                EventRegistration.user_id == user_id,
                EventRegistration.event_id == event_id,
                EventRegistration.status == RegistrationStatus.CONFIRMED.value
            )
        ).first()
    
    @staticmethod
    def create(db: Session, user_id: int, event_id: int, platform: Platform) -> EventRegistration:
        registration = EventRegistration(
            user_id=user_id,
            event_id=event_id,
            registered_via=platform.value,
            status=RegistrationStatus.CONFIRMED.value
        )
        db.add(registration)
        db.flush()
        return registration
    
    @staticmethod
    def get_confirmed_by_event(db: Session, event_id: int) -> List[EventRegistration]:
        return db.query(EventRegistration).filter(
            and_(
                EventRegistration.event_id == event_id,
                EventRegistration.status == RegistrationStatus.CONFIRMED.value
            )
        ).all()
    
    @staticmethod
    def get_user_registrations(db: Session, user_id: int) -> List[EventRegistration]:
        return db.query(EventRegistration).filter(
            and_(
                EventRegistration.user_id == user_id,
                EventRegistration.status == RegistrationStatus.CONFIRMED.value
            )
        ).join(Event).order_by(Event.date_time).all()
    
    @staticmethod
    def cancel(db: Session, registration: EventRegistration) -> EventRegistration:
        registration.status = RegistrationStatus.CANCELLED.value
        db.flush()
        return registration


class StateRepository:
    @staticmethod
    def get_state(db: Session, user_platform_id: str, platform: Platform) -> Optional[UserState]:
        return db.query(UserState).filter(
            and_(
                UserState.user_platform_id == user_platform_id,
                UserState.platform == platform.value
            )
        ).first()
    
    @staticmethod
    def set_state(db: Session, user_platform_id: str, platform: Platform, 
                  state: Optional[str], state_data: Optional[str] = None) -> UserState:
        user_state = StateRepository.get_state(db, user_platform_id, platform)
        
        if user_state:
            user_state.current_state = state
            user_state.state_data = state_data
            user_state.updated_at = datetime.utcnow()
        else:
            user_state = UserState(
                user_platform_id=user_platform_id,
                platform=platform.value,
                current_state=state,
                state_data=state_data
            )
            db.add(user_state)
        
        db.flush()
        return user_state
    
    @staticmethod
    def clear_state(db: Session, user_platform_id: str, platform: Platform):
        user_state = StateRepository.get_state(db, user_platform_id, platform)
        if user_state:
            db.delete(user_state)
            db.flush()
