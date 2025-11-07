from sqlalchemy.orm import Session
from typing import Optional
from database.repository import UserRepository
from database.models import User, Platform
from loguru import logger


class UserService:
    @staticmethod
    def get_or_create_telegram_user(db: Session, telegram_id: int, name: str, email: str) -> User:
        user = UserRepository.get_by_telegram_id(db, telegram_id)
        
        if user:
            logger.info(f"Existing user found: {user.id} ({user.email})")
            return user
        
        email_user = UserRepository.get_by_email(db, email)
        if email_user:
            if email_user.telegram_id is None:
                logger.info(f"Linking telegram_id {telegram_id} to existing user {email_user.id}")
                return UserRepository.update_telegram_id(db, email_user, telegram_id)
            else:
                logger.warning(f"Email {email} already linked to telegram_id {email_user.telegram_id}")
                raise ValueError(f"Email {email} уже привязан к другому Telegram аккаунту")
        
        logger.info(f"Creating new user: {name} ({email})")
        user = UserRepository.create(db, name=name, email=email, telegram_id=telegram_id)
        return user
    
    @staticmethod
    def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
        return UserRepository.get_by_telegram_id(db, telegram_id)
