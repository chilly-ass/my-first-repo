from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from loguru import logger

from database.connection import get_db
from database.models import Platform
from services.user_service import UserService
from services.event_service import EventService
from services.registration_service import RegistrationService
from services.fsm_service import FSMService
from telegram.states import RegistrationState
from telegram.keyboards import get_events_keyboard, get_confirmation_keyboard, get_main_menu_keyboard
from utils.validators import validate_email_address, validate_name
from utils.formatters import format_event, format_registration, format_event_list

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в систему регистрации на события!\n\n"
        "Используйте кнопки ниже для навигации:",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "ℹ️ <b>Справка по командам:</b>\n\n"
        "/start - Главное меню\n"
        "/events - Просмотр доступных событий\n"
        "/register - Регистрация на событие\n"
        "/my_registrations - Мои регистрации\n"
        "/help - Эта справка\n\n"
        "Или используйте кнопки меню для удобной навигации.",
        parse_mode=ParseMode.HTML
    )


@router.message(Command("events"))
async def cmd_events(message: Message):
    with get_db() as db:
        events = EventService.get_upcoming_events(db)
        
        if not events:
            await message.answer("На данный момент нет доступных событий.")
            return
        
        text = format_event_list(events)
        await message.answer(text, parse_mode=ParseMode.HTML)


@router.message(Command("register"))
async def cmd_register(message: Message):
    with get_db() as db:
        events = EventService.get_upcoming_events(db)
        
        if not events:
            await message.answer("На данный момент нет доступных событий для регистрации.")
            return
        
        user_id = str(message.from_user.id)
        FSMService.set_state(db, user_id, Platform.TELEGRAM, RegistrationState.CHOOSING_EVENT)
        
        await message.answer(
            "Выберите событие для регистрации:",
            reply_markup=get_events_keyboard(events)
        )


@router.message(Command("my_registrations"))
async def cmd_my_registrations(message: Message):
    with get_db() as db:
        user = UserService.get_user_by_telegram_id(db, message.from_user.id)
        
        if not user:
            await message.answer("У вас пока нет регистраций. Используйте /register для регистрации на событие.")
            return
        
        registrations = RegistrationService.get_user_registrations(db, user)
        
        if not registrations:
            await message.answer("У вас пока нет активных регистраций.")
            return
        
        text = "<b>Ваши регистрации:</b>\n\n"
        for reg in registrations:
            text += f"• {reg.event.title}\n"
            text += f"  🕐 {reg.event.date_time.strftime('%d.%m.%Y %H:%M')}\n"
            text += f"  📍 {reg.event.location}\n\n"
        
        await message.answer(text, parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("menu:"))
async def handle_menu(callback: CallbackQuery):
    action = callback.data.split(":")[1]
    
    if action == "events":
        await cmd_events(callback.message)
    elif action == "my_registrations":
        await cmd_my_registrations(callback.message)
    elif action == "help":
        await cmd_help(callback.message)
    
    await callback.answer()


@router.callback_query(F.data.startswith("event:"))
async def handle_event_selection(callback: CallbackQuery):
    event_id = int(callback.data.split(":")[1])
    user_id = str(callback.from_user.id)
    
    with get_db() as db:
        event = EventService.get_event_by_id(db, event_id)
        
        if not event:
            await callback.answer("Событие не найдено", show_alert=True)
            return
        
        available = event.max_participants - len(event.registrations)
        if available <= 0:
            await callback.answer("К сожалению, все места заняты", show_alert=True)
            return
        
        FSMService.set_state(db, user_id, Platform.TELEGRAM, RegistrationState.ENTERING_NAME, 
                           {"event_id": event_id})
        
        await callback.message.answer(
            f"Вы выбрали: <b>{event.title}</b>\n\n"
            "Пожалуйста, введите ваше имя:",
            parse_mode=ParseMode.HTML
        )
        await callback.answer()


@router.message(F.text)
async def handle_text_input(message: Message):
    user_id = str(message.from_user.id)
    
    with get_db() as db:
        state = FSMService.get_state(db, user_id, Platform.TELEGRAM)
        
        if not state:
            await message.answer(
                "Используйте /start для начала работы или /help для справки."
            )
            return
        
        if state == RegistrationState.ENTERING_NAME:
            await handle_name_input(message, db, user_id)
        elif state == RegistrationState.ENTERING_EMAIL:
            await handle_email_input(message, db, user_id)


async def handle_name_input(message: Message, db, user_id: str):
    is_valid, result = validate_name(message.text)
    
    if not is_valid:
        await message.answer(f"❌ {result}\n\nПожалуйста, введите корректное имя:")
        return
    
    FSMService.update_state_data(db, user_id, Platform.TELEGRAM, {"name": result})
    FSMService.set_state(db, user_id, Platform.TELEGRAM, RegistrationState.ENTERING_EMAIL, 
                        FSMService.get_state_data(db, user_id, Platform.TELEGRAM))
    
    await message.answer("Отлично! Теперь введите ваш email:")


async def handle_email_input(message: Message, db, user_id: str):
    is_valid, result = validate_email_address(message.text)
    
    if not is_valid:
        await message.answer(
            f"❌ Некорректный email: {result}\n\n"
            "Пожалуйста, введите корректный email адрес:"
        )
        return
    
    data = FSMService.get_state_data(db, user_id, Platform.TELEGRAM)
    data["email"] = result
    
    event = EventService.get_event_by_id(db, data["event_id"])
    
    if not event:
        await message.answer("❌ Ошибка: событие не найдено")
        FSMService.clear_state(db, user_id, Platform.TELEGRAM)
        return
    
    FSMService.set_state(db, user_id, Platform.TELEGRAM, RegistrationState.CONFIRMING, data)
    
    confirmation_text = (
        f"📋 <b>Подтвердите регистрацию:</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📧 Email: {data['email']}\n\n"
        f"📅 Событие: <b>{event.title}</b>\n"
        f"🕐 Дата: {event.date_time.strftime('%d.%m.%Y %H:%M')}\n"
        f"📍 Место: {event.location}\n\n"
        f"Всё верно?"
    )
    
    await message.answer(confirmation_text, parse_mode=ParseMode.HTML, reply_markup=get_confirmation_keyboard())


@router.callback_query(F.data.startswith("confirm:"))
async def handle_confirmation(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    confirmation = callback.data.split(":")[1]
    
    with get_db() as db:
        state = FSMService.get_state(db, user_id, Platform.TELEGRAM)
        
        if state != RegistrationState.CONFIRMING:
            await callback.answer("Ошибка: неверное состояние", show_alert=True)
            return
        
        data = FSMService.get_state_data(db, user_id, Platform.TELEGRAM)
        
        if confirmation == "no":
            FSMService.clear_state(db, user_id, Platform.TELEGRAM)
            await callback.message.answer("❌ Регистрация отменена. Используйте /register для новой попытки.")
            await callback.answer()
            return
        
        try:
            telegram_id = callback.from_user.id
            user = UserService.get_or_create_telegram_user(db, telegram_id, data["name"], data["email"])
            
            event = EventService.get_event_by_id(db, data["event_id"])
            registration = RegistrationService.register_user_for_event(db, user, event, Platform.TELEGRAM)
            
            FSMService.clear_state(db, user_id, Platform.TELEGRAM)
            
            await callback.message.answer(
                format_registration(registration),
                parse_mode=ParseMode.HTML
            )
            await callback.answer("✅ Регистрация успешна!")
            
        except ValueError as e:
            await callback.message.answer(f"❌ Ошибка: {str(e)}")
            FSMService.clear_state(db, user_id, Platform.TELEGRAM)
            await callback.answer()
        except Exception as e:
            logger.error(f"Registration error: {e}")
            await callback.message.answer("❌ Произошла ошибка при регистрации. Попробуйте позже.")
            FSMService.clear_state(db, user_id, Platform.TELEGRAM)
            await callback.answer()
