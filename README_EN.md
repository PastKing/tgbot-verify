# SheerID Auto-Verification Telegram Bot

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> 🤖 Automated SheerID Student/Teacher Verification Telegram Bot
>
> Based on [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond's legacy code with improvements

[简体中文](README.md) | [繁體中文](README_TW.md) | English

---

## 📋 Overview

A Python-based Telegram bot that automates SheerID student/teacher identity verification for multiple platforms. The bot automatically generates identity information, creates verification documents, and submits them to the SheerID platform, significantly simplifying the verification process.

### 🎯 Supported Services

| Command | Service | Type | Status |
|---------|---------|------|--------|
| `/verify` | Gemini One Pro | Teacher | ✅ Complete |
| `/verify2` | ChatGPT Teacher K12 | Teacher | ✅ Complete |
| `/verify3` | Spotify Student | Student | ✅ Complete |
| `/verify4` | Bolt.new Teacher | Teacher | ✅ Complete |
| `/verify5` | YouTube Premium Student | Student | ⚠️ In Progress |

> **⚠️ Before Use**: The `programId` in each module's `config.py` may need periodic updates. If verification keeps failing, please update accordingly. See the Configuration section below.

### ✨ Key Features

- 🚀 **Automated Process**: One-click info generation, document creation, and submission
- 🎨 **Smart Generation**: Auto-generates student/teacher ID PNG images
- 💰 **Points System**: Check-ins, invitations, and redemption codes
- 🔐 **Secure & Reliable**: MySQL database with environment variable configuration
- ⚡ **Concurrency Control**: Intelligent management of concurrent requests for stability
- 👥 **Admin Features**: Complete user and points management system

---

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Bot Framework**: python-telegram-bot 20.0+
- **Database**: MySQL 5.7+
- **Browser Automation**: Playwright
- **HTTP Client**: httpx
- **Image Processing**: Pillow, reportlab, xhtml2pdf
- **Environment Management**: python-dotenv

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Environment Variables

Copy `env.example` to `.env` and fill in the configuration:

```env
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel
ADMIN_USER_ID=your_admin_id

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=tgbot_verify
```

### 4. Start Bot

```bash
python bot.py
```

---

## 🐳 Docker Deployment

```bash
cp env.example .env
nano .env
docker-compose up -d
docker-compose logs -f
```

Manual build:

```bash
docker build -t tgbot-verify .
docker run -d --name tgbot-verify --env-file .env -v $(pwd)/logs:/app/logs tgbot-verify
```

---

## 📖 Usage

### User Commands

```
/start              # Start (register)
/about              # Learn about bot features
/balance            # Check points balance
/qd                 # Daily check-in (+1 point)
/invite             # Generate invitation link (+2 points/person)
/use <code>         # Redeem points with code
/verify <link>      # Gemini One Pro verification
/verify2 <link>     # ChatGPT Teacher K12 verification
/verify3 <link>     # Spotify Student verification
/verify4 <link>     # Bolt.new Teacher verification
/verify5 <link>     # YouTube Premium Student verification
/help               # View help
```

### Admin Commands

```
/addbalance <user_id> <points>               # Add user points
/block <user_id>                             # Block user
/white <user_id>                             # Unblock user
/blacklist                                   # View blacklist
/genkey <code> <points> [times] [days]       # Generate redemption code
/listkeys                                    # View redemption codes
/broadcast <text>                            # Broadcast notification
```

### Verification Process

1. Visit the service's verification page and start the verification flow
2. Copy the full URL from browser address bar (including `verificationId`)
3. Send to bot: `/verify3 https://services.sheerid.com/verify/xxx/?verificationId=yyy`
4. Wait for processing — review usually completes within minutes

---

## 📁 Project Structure

```
tgbot-verify/
├── bot.py                  # Main bot program
├── config.py               # Global configuration
├── database_mysql.py       # MySQL database management
├── env.example             # Environment variables template
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── handlers/               # Command handlers
│   ├── user_commands.py
│   ├── admin_commands.py
│   └── verify_commands.py
├── one/                    # Gemini One Pro module
├── k12/                    # ChatGPT K12 module
├── spotify/                # Spotify Student module
├── youtube/                # YouTube Premium module
├── Boltnew/                # Bolt.new module
├── military/               # ChatGPT Military verification docs
└── utils/                  # Utility functions
    ├── messages.py
    ├── concurrency.py
    └── checks.py
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Telegram Bot Token |
| `ADMIN_USER_ID` | ✅ | Admin Telegram ID |
| `MYSQL_HOST` | ✅ | MySQL host address |
| `MYSQL_USER` | ✅ | MySQL username |
| `MYSQL_PASSWORD` | ✅ | MySQL password |
| `MYSQL_DATABASE` | ✅ | Database name |
| `CHANNEL_USERNAME` | ❌ | Channel username (default: pk_oa) |
| `CHANNEL_URL` | ❌ | Channel link |
| `MYSQL_PORT` | ❌ | MySQL port (default: 3306) |

### Updating programId

If verification keeps failing, the `programId` is likely outdated. To update:

1. Open the service's verification page, press F12 → Network tab
2. Start verification, find the `https://services.sheerid.com/rest/v2/verification/` request
3. Extract `programId` and update the corresponding module's `config.py`

Files to update: `one/config.py` | `k12/config.py` | `spotify/config.py` | `youtube/config.py` | `Boltnew/config.py`

### Points Configuration (config.py)

```python
VERIFY_COST = 1        # Points cost per verification
CHECKIN_REWARD = 1     # Daily check-in reward
INVITE_REWARD = 2      # Invitation reward
REGISTER_REWARD = 1    # Registration reward
```

---

## 🤝 Contact & Collaboration

- 📢 **Telegram Channel**: [@pk_oa](https://t.me/pk_oa)
- 📧 **Email**: pastking69@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

Open to collaboration — feel free to reach out via the above channels.

---

## 🛠️ Contributing / Secondary Development

Welcome to fork and build upon this project. Please:

- Keep original repository link and author credits
- Follow MIT License — derivative projects must also be open source
- Free for personal use; commercial use is at your own risk

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Thanks to [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond for the legacy code foundation
- Thanks to all developers who contributed to this project

---

## 📊 Statistics

[![Star History Chart](https://api.star-history.com/svg?repos=PastKing/tgbot-verify&type=Date)](https://star-history.com/#PastKing/tgbot-verify&Date)

---

<p align="center">
  <strong>⭐ If this project helps you, please give it a Star!</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/PastKing">PastKing</a>
</p>
