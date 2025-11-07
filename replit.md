# Event Registration Bot

## Overview
Telegram bot for event registration with automated notifications built with FastAPI, aiogram, and PostgreSQL.

## Project Status
- **Created**: November 07, 2025
- **Current State**: MVP implementation - Telegram-only bot with PostgreSQL storage

## Architecture

### Stack
- **Backend**: FastAPI (webhook server)
- **Bot Framework**: aiogram 3.x (Telegram)
- **Database**: PostgreSQL (Replit-hosted)
- **Scheduler**: APScheduler (event reminders)
- **Validation**: Pydantic + email-validator
- **Logging**: Loguru

### Features
1. Event browsing and registration
2. FSM-based registration flow (name → email → confirmation)
3. User management with email-based account linking
4. Automated reminders (24h and 1h before events)
5. Health check endpoint

## Project Structure
```
├── main.py                    # FastAPI application entry point
├── config.py                  # Settings management
├── database/
│   ├── models.py             # SQLAlchemy models
│   ├── connection.py         # Database connection
│   └── repository.py         # Data access layer
├── services/
│   ├── user_service.py       # User business logic
│   ├── event_service.py      # Event business logic
│   ├── registration_service.py
│   ├── fsm_service.py        # State management
│   └── notification_service.py
├── telegram/
│   ├── handlers.py           # Bot command handlers
│   ├── states.py             # FSM states
│   └── keyboards.py          # Inline keyboards
├── scheduler/
│   ├── scheduler.py          # APScheduler setup
│   └── tasks.py              # Reminder tasks
└── utils/
    ├── validators.py         # Input validation
    └── formatters.py         # Message formatting
```

## Database Schema

### Tables
- **users**: User accounts (telegram_id, name, email, whatsapp_phone)
- **events**: Events with date/time, location, max participants
- **event_registrations**: User-event registrations with status
- **user_states**: FSM state storage

## Configuration

### Required Environment Variables
- `BOT_TOKEN`: Telegram bot token from @BotFather
- `WEBHOOK_URL`: Public URL for webhook (Replit URL)
- `DATABASE_URL`: PostgreSQL connection string (auto-configured)

### Optional Variables
- `WEBHOOK_PATH`: Webhook endpoint path (default: /telegram)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `LOG_LEVEL`: Logging level (default: INFO)

## Setup Instructions

1. Get a Telegram bot token from [@BotFather](https://t.me/botfather)
2. Set environment variables in Replit Secrets:
   - `BOT_TOKEN`: Your bot token
   - `WEBHOOK_URL`: Your Replit app URL (e.g., https://your-repl.repl.co)
3. Run `add_sample_events.py` to populate the database with sample events
4. Start the application

## Commands

### User Commands
- `/start` - Main menu
- `/events` - View available events
- `/register` - Register for an event
- `/my_registrations` - View your registrations
- `/help` - Show help

### Admin Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `POST /telegram` - Webhook endpoint

## Notification System

APScheduler runs hourly checks:
- **24-hour reminder**: Sent to all registered users
- **1-hour reminder**: Final reminder before event

## Future Enhancements
- WhatsApp bot integration (PyWa)
- Admin panel for event management
- Event cancellation feature
- Registration limits per user
- Email notifications
- Sentry error monitoring
- Redis for improved FSM performance

## Notes
- Uses webhook mode (not polling) for Telegram
- State management stored in PostgreSQL
- Account linking via email address
- Timezone: UTC (timestamps stored in UTC)
