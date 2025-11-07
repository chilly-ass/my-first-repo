from datetime import datetime, timedelta
from database.connection import init_db, get_db
from database.repository import EventRepository
from loguru import logger

logger.info("Adding sample events...")

init_db()

sample_events = [
    {
        "title": "Python Workshop",
        "description": "Изучение основ Python программирования",
        "date_time": datetime.now() + timedelta(days=7),
        "location": "Онлайн",
        "max_participants": 30
    },
    {
        "title": "Web Development Meetup",
        "description": "Обсуждение современных веб-технологий",
        "date_time": datetime.now() + timedelta(days=14),
        "location": "Москва, ул. Примерная 1",
        "max_participants": 50
    },
    {
        "title": "AI & Machine Learning Conference",
        "description": "Конференция по искусственному интеллекту",
        "date_time": datetime.now() + timedelta(days=30),
        "location": "Санкт-Петербург",
        "max_participants": 100
    },
    {
        "title": "Networking Event",
        "description": "Networking для IT специалистов",
        "date_time": datetime.now() + timedelta(hours=25),
        "location": "Онлайн",
        "max_participants": 20
    }
]

with get_db() as db:
    for event_data in sample_events:
        event = EventRepository.create(db, **event_data)
        logger.info(f"Created event: {event.title} (ID: {event.id})")

logger.info(f"Successfully added {len(sample_events)} sample events!")
