from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import Event, EventRegistration


def format_event(event: 'Event') -> str:
    return (
        f"📅 <b>{event.title}</b>\n"
        f"📝 {event.description}\n"
        f"🕐 {event.date_time.strftime('%d.%m.%Y %H:%M')}\n"
        f"📍 {event.location}\n"
        f"👥 Мест: {event.max_participants - len(event.registrations)}/{event.max_participants}"
    )


def format_registration(registration: 'EventRegistration') -> str:
    event = registration.event
    return (
        f"✅ Вы зарегистрированы на событие:\n\n"
        f"{format_event(event)}\n\n"
        f"Мы отправим вам напоминание за 24 часа и за 1 час до начала."
    )


def format_event_list(events: list['Event']) -> str:
    if not events:
        return "На данный момент нет доступных событий."
    
    result = "<b>Доступные события:</b>\n\n"
    for i, event in enumerate(events, 1):
        result += f"{i}. {event.title}\n"
        result += f"   🕐 {event.date_time.strftime('%d.%m.%Y %H:%M')}\n"
        result += f"   👥 Свободных мест: {event.max_participants - len(event.registrations)}\n\n"
    
    return result


def format_reminder(event: 'Event', hours_before: int) -> str:
    return (
        f"⏰ <b>Напоминание!</b>\n\n"
        f"Событие <b>{event.title}</b> начнется через {hours_before} {'час' if hours_before == 1 else 'часа'}!\n\n"
        f"🕐 Время: {event.date_time.strftime('%d.%m.%Y %H:%M')}\n"
        f"📍 Место: {event.location}\n\n"
        f"До встречи!"
    )
