from sqlalchemy.orm import Session
from typing import Optional
import json
from database.repository import StateRepository
from database.models import Platform
from loguru import logger


class FSMService:
    @staticmethod
    def get_state(db: Session, user_platform_id: str, platform: Platform) -> Optional[str]:
        state = StateRepository.get_state(db, user_platform_id, platform)
        return state.current_state if state else None
    
    @staticmethod
    def get_state_data(db: Session, user_platform_id: str, platform: Platform) -> Optional[dict]:
        state = StateRepository.get_state(db, user_platform_id, platform)
        if state and state.state_data:
            try:
                return json.loads(state.state_data)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in state_data for {user_platform_id}")
                return None
        return None
    
    @staticmethod
    def set_state(db: Session, user_platform_id: str, platform: Platform, state: str, data: Optional[dict] = None):
        state_data = json.dumps(data) if data else None
        StateRepository.set_state(db, user_platform_id, platform, state, state_data)
        logger.debug(f"Set state {state} for {user_platform_id}")
    
    @staticmethod
    def clear_state(db: Session, user_platform_id: str, platform: Platform):
        StateRepository.clear_state(db, user_platform_id, platform)
        logger.debug(f"Cleared state for {user_platform_id}")
    
    @staticmethod
    def update_state_data(db: Session, user_platform_id: str, platform: Platform, data: dict):
        current_state = FSMService.get_state(db, user_platform_id, platform)
        if current_state:
            current_data = FSMService.get_state_data(db, user_platform_id, platform) or {}
            current_data.update(data)
            FSMService.set_state(db, user_platform_id, platform, current_state, current_data)
