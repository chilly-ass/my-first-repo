# Testing Guide

## Testing Your Telegram Bot

### 1. Find Your Bot in Telegram

1. Open Telegram on your phone or desktop
2. Search for your bot using the username you gave it when creating with @BotFather
3. Click "START" to begin

### 2. Test Basic Commands

```
/start     → Should show main menu with buttons
/events    → Should show list of available events
/help      → Should show help information
```

### 3. Test Registration Flow

1. Click "📝 Register" or send `/register`
2. Choose an event from the list
3. Enter your name when prompted
4. Enter your email address
5. Confirm your registration
6. You should receive a confirmation message

### 4. Test My Registrations

1. Send `/my_registrations` command
2. You should see your registered events

### 5. Test Event Display

The event list should show:
- Event title
- Date and time
- Available spots remaining

### 6. Verify Webhook

Check that the webhook is active:

```bash
python setup_webhook.py
```

You should see:
```
✅ Webhook successfully set to: https://your-domain/telegram
Current webhook: https://your-domain/telegram
Pending updates: 0
```

### 7. Check Application Logs

View the Replit console to monitor:
- Incoming messages
- User registrations
- Errors (if any)
- Scheduler activity

### 8. API Health Check

Visit these URLs in your browser:
- `https://your-domain/` - API info
- `https://your-domain/health` - Health check

### Expected Events

The database includes 4 sample events:
1. Python Workshop (in 7 days)
2. Web Development Meetup (in 14 days)
3. AI & Machine Learning Conference (in 30 days)
4. Networking Event (in 25 hours - should trigger 24h reminder soon!)

### Troubleshooting

**Bot doesn't respond:**
- Verify BOT_TOKEN is set correctly
- Check webhook status
- View console logs for errors

**Registration fails:**
- Check if event has available spots
- Verify email format is valid
- Check console logs for specific error

**No reminders:**
- APScheduler runs every hour
- Reminders sent 24h and 1h before events
- Check event dates are in the future

## Manual Testing Checklist

- [ ] Bot responds to /start
- [ ] Can view events list
- [ ] Can complete full registration flow
- [ ] Name validation works (min 2 chars)
- [ ] Email validation works
- [ ] Confirmation buttons work
- [ ] Can view my registrations
- [ ] Cannot register twice for same event
- [ ] Cannot register when event is full
- [ ] Help command shows all commands
