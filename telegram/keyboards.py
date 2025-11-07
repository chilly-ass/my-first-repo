from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from database.models import Event


def get_events_keyboard(events: List[Event]) -> InlineKeyboardMarkup:
    buttons = []
    for event in events:
        available_spots = event.max_participants - len(event.registrations)
        button_text = f"{event.title} ({available_spots} мест)"
        buttons.append([InlineKeyboardButton(
            text=button_text,
            callback_data=f"event:{event.id}"
        )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm:yes"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="confirm:no")
        ]
    ])


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Доступные события", callback_data="menu:events")],
        [InlineKeyboardButton(text="📝 Мои регистрации", callback_data="menu:my_registrations")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="menu:help")]
    ])
