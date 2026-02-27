# AdGuardian Bot 🛡️

An advanced Discord bot that intelligently detects and prevents advertisements, self-promotion, and spam with an automated warning system, message deletion, and user muting.

## Features

✅ **Smart Advertisement Detection**
- Regex-based pattern matching for promotional content
- Blocks URLs (http, www, bit.ly, discord.gg)
- Detects call-to-action phrases (check out, visit, subscribe)
- Identifies self-promotion (my server, my bot, my project)
- Blocks marketing terms (promo code, discount, affiliate)
- Blocks major streaming platforms (YouTube, Twitch, Patreon, etc.)

✅ **Progressive Penalty System**
- **1st Warning**: Message deleted + Private DM warning
- **2nd Warning**: Message deleted + Stronger warning in channel
- **3rd+ Violation**: User automatically muted for 24 hours

✅ **Database Persistence**
- SQLite database stores warnings per user per guild
- Warnings persist between bot restarts

✅ **Moderator Commands**
- `!warnings @user` - Check user's warning count
- `!reset_warnings @user` - Reset user's warnings

✅ **Admin/Mod Bypass**
- Administrators and Moderators can post promotional content without triggering the filter

✅ **24/7 Availability**
- Can be hosted on Replit for free, always online
- Auto-restart on crashes

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Discord bot token

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/BisheshJoshi/AdGuardian-Bot.git
cd AdGuardian-Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Add your bot token to `.env`:
```
DISCORD_TOKEN=your_bot_token_here
```

5. Run the bot:
```bash
python main.py
```

### Replit Setup (Recommended - Free 24/7 Hosting)

1. Go to [https://replit.com](https://replit.com)
2. Click "Create Repl" and select "Python"
3. Paste the repository URL or upload files
4. Create `.env` file with your bot token
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `python main.py`
7. Bot runs 24/7 automatically!

## Getting Your Bot Token

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it
3. Go to "Bot" → "Add Bot"
4. Copy the token (keep it secret!)
5. Enable these Intents:
   - Message Content Intent
   - Server Members Intent
6. Under "OAuth2" → "URL Generator":
   - Select scope: `bot`
   - Select permissions:
     - Send Messages
     - Delete Messages
     - Moderate Members
     - Read Message History
7. Copy the generated URL and open it to invite the bot

## Commands

### Moderator Commands

| Command | Usage | Permission |
|---------|-------|------------|
| `!warnings @user` | Check user's warning count | Moderator+ |
| `!reset_warnings @user` | Reset user's warnings | Moderator+ |

## How It Works

1. **Message Scanning**: Every message is scanned against advertisement patterns
2. **Admin Check**: If sender is admin/mod, message is allowed
3. **Pattern Matching**: Message checked against regex patterns and blocked domains
4. **Action Taken**:
   - Message is deleted
   - User gets warning (stored in database)
   - User receives DM notification
   - Channel notification (depends on warning count)
5. **Progressive Punishment**:
   - 1st: Warning DM
   - 2nd: Stronger warning in channel
   - 3rd: 24-hour mute

## Configuration

Edit `main.py` to customize:

```python
# Promotion patterns (regex)
PROMO_PATTERNS = [
    r'(?:http|www|bit\.ly|discord\.gg)',
    r'(?:check out|click here|buy now|visit|subscribe)',
    r'(?:my server|my bot|my project|my website|my channel)',
    r'(?:promo code|discount|affiliate|ref code)',
    r'(?:dm me|dm for|dm to)',
]

# Blocked domains
BLOCKED_DOMAINS = [
    'twitch.tv', 'youtube.com', 'tiktok.com',
    'patreon.com', 'kickstarter.com', 'gofundme.com',
    'amazon.com', 'etsy.com',
]
```

## Database

The bot uses SQLite with a `warnings` table:

| Column | Type | Purpose |
|--------|------|----------|
| user_id | INTEGER | Discord user ID |
| guild_id | INTEGER | Discord server ID |
| warning_count | INTEGER | Number of warnings |

## Troubleshooting

**Bot not responding?**
- Check if bot has Send Messages permission
- Verify bot token is correct
- Ensure Message Content Intent is enabled

**Warnings not saving?**
- Check if `warnings.db` file exists
- Verify database permissions
- Restart the bot

**Bot muting wrong users?**
- Verify Moderate Members permission
- Check bot role is above user roles
- Ensure bot has Timeout permission

## Support

If you encounter issues:
1. Check bot permissions in your server
2. Verify Discord Developer Portal settings
3. Check bot token is correct
4. Ensure requirements are installed

## License

MIT License - Feel free to use and modify

## Author

Created with ❤️ for Discord community moderation

---

**Made with discord.py** 🐍
