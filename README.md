# 🤖 Telegram Moderation Bot

<div align="center">

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A powerful, feature-rich Telegram bot for seamless group moderation**

[Features](#-features) • [Installation](#-installation) • [Commands](#-commands) • [Deployment](#-deployment)

</div>

---

## ✨ Features

### 🛡️ Moderation Tools
- **Warning System** - Track user violations with auto-ban on limit
- **User Control** - Kick, ban, mute, and unmute members
- **Message Management** - Delete and purge messages in bulk
- **Content Locks** - Restrict media, stickers, links, and more
- **Admin Management** - Promote, demote, and set custom titles

### 📝 Customization
- **Custom Filters** - Auto-reply to specific keywords
- **Word Blacklist** - Block unwanted words with configurable actions
- **Welcome & Goodbye** - Greet new members with text or photos
- **Group Rules** - Set and display community guidelines
- **Permissions** - Configure command access levels

### 📊 Data Storage
All data is stored locally in JSON files:
- `warnings.json` - User warning records per group
- `settings.json` - Group configurations (rules, welcome/goodbye messages, max warn actions)
- `filters.json` - Custom auto-reply filters per group
- `blacklist.json` - Blacklisted words and phrases per group
- `locks.json` - Message type restrictions per group

---

## 🚀 Installation

### Step 1: Get Your Bot Token

1. Open Telegram and search for [BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

### Step 2: Get Your User ID

1. Search for [userinfobot](https://t.me/userinfobot) on Telegram
2. Send `/start` to the bot
3. Copy your User ID from the response

<div align="center">
<img src="https://i.ibb.co/yF9rBYXR/photo-2025-10-07-10-19-38.jpg" alt="UserInfoBot Example" width="400">
</div>

### Step 3: Setup Environment Variables

1. Copy `.env.example` to `.env`
2. Add your credentials:

```env
BOT_TOKEN=your_bot_token_here
OWNER_ID=your_user_id_here
MAX_WARNS=3
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Bot

```bash
python bot.py
```

---

## 👥 Add Bot to Your Group

1. Add your bot to your Telegram group
2. Promote the bot to admin with these permissions:
   - ✅ Delete messages
   - ✅ Ban users
   - ✅ Invite users via link
   - ✅ Pin messages
   - ✅ Manage chat

---

## ⚙️ Configuration

### Permissions System

Control who can use specific commands by editing `permissions.json` or using the command:

```
/setpermission <command> <user|admin>
```

- `user` - Anyone can use the command
- `admin` - Only group admins can use

### Max Warning Actions

Configure what happens when users reach the warning limit:

```
/maxwarnaction ban          # Permanently ban the user
/maxwarnaction kick         # Remove from group
/maxwarnaction tempban 1h   # Temporary ban (1h, 30m, 1d)
```

### Blacklist Actions

Set the behavior when blacklisted words are detected:

```
/blacklistwordaction delete            # Delete message only
/blacklistwordaction delete+warn       # Delete and warn user
/blacklistwordaction delete+notify     # Delete and notify admins
```

---

## 📋 Commands

### 🛡️ Moderation (Admin Only)

| Command | Description | Example |
|---------|-------------|---------|
| `/warn @user [reason]` | Issue a warning | `/warn @john Spamming` |
| `/kick @user [reason]` | Remove user from group | `/kick @john` |
| `/ban @user [reason]` | Ban user permanently | `/ban @john Repeated violations` |
| `/unban @user` | Unban a user | `/unban @john` |
| `/mute @user [duration]` | Mute user temporarily | `/mute @john 1h` |
| `/unmute @user` | Unmute a user | `/unmute @john` |

### 💬 Message Management (Admin Only)

| Command | Description |
|---------|-------------|
| `/delete` | Delete the replied message |
| `/purge <number>` | Delete last X messages (max 100) |

### 🔒 Content Locks (Admin Only)

| Command | Description |
|---------|-------------|
| `/lock <type>` | Lock specific message types |
| `/unlock <type>` | Unlock message types |
| `/lockall` | Lock all message types |
| `/unlockall` | Unlock all message types |

**Lock types:** `media`, `stickers`, `gifs`, `links`, `forward`, `bot`, `inline`

### 👔 Admin Tools

| Command | Description |
|---------|-------------|
| `/promote @user [title]` | Promote user to admin |
| `/demote @user` | Remove admin privileges |
| `/settitle @user <title>` | Set custom admin title |
| `/invitelink` | Get group invite link |

### 📌 Pin Management (Admin Only)

| Command | Description |
|---------|-------------|
| `/pin` | Pin the replied message |
| `/unpin` | Unpin the replied message |
| `/unpinall` | Unpin all messages |

### ℹ️ Information

| Command | Description |
|---------|-------------|
| `/info @user` | View user information |
| `/warns @user` | Check user warnings |
| `/resetwarns @user` | Clear user warnings (Admin) |

### ⚙️ Group Settings (Admin Only)

| Command | Description |
|---------|-------------|
| `/setrules <text>` | Set group rules |
| `/rules` | Display group rules |
| `/setwelcome <text>` | Set welcome message (reply to photo for image) |
| `/welcome on/off` | Toggle welcome messages |
| `/setgoodbye <text>` | Set goodbye message (reply to photo for image) |
| `/goodbye on/off` | Toggle goodbye messages |

### 🔍 Filters & Blacklist

| Command | Description |
|---------|-------------|
| `/filter <keyword> <response>` | Add auto-reply filter (Admin) |
| `/filters` | List all active filters |
| `/stop <keyword>` | Remove a filter (Admin) |
| `/blacklist <words>` | Add words to blacklist (Admin) |
| `/unblacklist <words>` | Remove from blacklist (Admin) |
| `/blacklisted` | Show all blacklisted words |

---

## 🌐 Deployment

### Deploy on Render / Railway / VPS

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd telegram-moderation-bot
   ```

2. **Set environment variables** in your hosting platform:
   - `BOT_TOKEN`
   - `OWNER_ID`
   - `MAX_WARNS`

3. **Start the bot**
   ```bash
   python bot.py
   ```

4. **Keep it running** using:
   - **Systemd** (Linux)
   - **Supervisor** (Unix)
   - **PM2** (Node.js process manager)
   - Platform-specific tools (Render auto-restart, Railway persistent processes)

---

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Verify bot token is correct
- Ensure bot has admin permissions in the group
- Check bot logs for error messages

**Commands not working:**
- Check if command permissions are set correctly
- Verify you're replying to messages when required (e.g., `/delete`, `/pin`)
- Ensure bot has necessary admin rights

**Data not persisting:**
- Verify write permissions for JSON files
- Check if `data/` directory exists
- Review logs for file system errors

---

## 📄 License

This project is licensed under the MIT License.

---

## 🌟 Premium Features

Want advanced features like anti-spam, raid protection, analytics, and more?

[**Unlock Premium Features**](https://t.me/unikruzng) 🚀

---

## 💬 Support

Need help or have questions?

[**Talk to me**](https://t.me/unikruzng) - Get direct support from the developer

For technical issues:
- Check the bot logs for detailed error messages
- Verify all admin permissions are correctly configured
- Ensure environment variables are properly set

---

<div align="center">

**Made with ❤️ by Firekid**

⭐ Star this repo if you find it helpful!

</div>
