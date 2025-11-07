# 🤖 Event Registration Telegram Bot

Telegram bot for event registration with automated notifications.

## ✨ Features

- 📋 Browse upcoming events
- 📝 Register for events with name and email
- ✅ Smart FSM-based registration flow
- ⏰ Automated reminders (24h and 1h before events)
- 💾 PostgreSQL database for persistent storage
- 🔗 Email-based account linking (future WhatsApp integration ready)

## 🚀 Quick Start

### 1. Get Your Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the bot token you receive

### 2. Configure Secrets

Add the following secret in Replit Secrets:
- `BOT_TOKEN` - Your Telegram bot token

### 3. Setup & Run

The bot is already running! Just:

1. Open Telegram and search for your bot
2. Send `/start` to begin

## 📱 Bot Commands

- `/start` - Main menu with navigation buttons
- `/events` - View all upcoming events
- `/register` - Register for an event
- `/my_registrations` - View your active registrations
- `/help` - Show help information

## 🔄 Registration Flow

1. Choose an event from the list
2. Enter your name
3. Enter your email
4. Confirm your registration
5. Done! You'll receive reminders before the event

## 🛠️ Maintenance

### Add New Events

Edit and run `add_sample_events.py` to add more events to the database.

### Check Logs

View logs in the Replit console to monitor bot activity and debug issues.

### Database

The bot uses PostgreSQL for data storage. All user data, events, and registrations are persisted automatically.

## 📊 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /telegram` - Telegram webhook (automatically configured)

## 🏗️ Architecture

```
FastAPI Server (Webhook)
├── Telegram Bot (aiogram)
├── PostgreSQL Database
├── APScheduler (Reminders)
└── FSM State Management
```

## 📝 Database Schema

- **users** - User accounts with Telegram ID and email
- **events** - Events with date, location, capacity
- **event_registrations** - User-event registrations
- **user_states** - FSM state tracking

## 🔮 Future Enhancements

- WhatsApp bot integration
- Admin panel for event management
- Event cancellation feature
- Email notifications
- Multi-language support
- User timezone handling

## 🐛 Troubleshooting

**Bot doesn't respond:**
- Check that BOT_TOKEN is set correctly
- Verify the webhook is active: run `python setup_webhook.py`
- Check logs for errors

**Database errors:**
- The database is automatically created on startup
- Check DATABASE_URL environment variable

## 📄 License

This project is created for educational purposes.
