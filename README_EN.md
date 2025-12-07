# SheerID Auto Verification Bot

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Telegram](https://img.shields.io/badge/telegram-bot-blue)

**An automated Telegram bot for completing SheerID student/teacher verification**

English | [简体中文](./README.md)

</div>

---

## 📢 Important Notice

> This project is an **early version** of [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) (GGBond)  
> **Suitable for personal use, please optimize for commercial use**  
> For educational purposes only, do not use for illegal activities

---

## ✨ Project Overview

This is an automated verification tool based on Python Telegram Bot that can automatically complete student/teacher identity verification processes on the SheerID platform. By simulating real user operations, it automatically generates and submits verification documents, greatly simplifying the verification process.

### 🎯 Supported Verification Services

| Service | Command | Description |
|---------|---------|-------------|
| ✅ Gemini One Pro | `/verify` | Google Gemini Student Verification |
| ✅ ChatGPT Teacher K12 | `/verify2` | OpenAI Teacher Verification |
| ✅ Bolt.new Teacher | `/verify4` | Bolt.new Teacher Verification (Fully Automated) |
| ❌ ~~Spotify Student~~ | ~~`/verify3`~~ | **Removed** |

> **Note**: Spotify verification module has been removed from this version

---

## 🚀 Key Features

- 🤖 **Fully Automated**: One-click submission, automatic document generation and verification
- ⚡ **High Concurrency**: Support multiple users simultaneously without interference
- 💾 **MySQL Database**: Enterprise-level data storage, support large-scale users
- 🎨 **Smart Document Generation**: High-quality verification documents rendered using Playwright
- 🔐 **Points System**: Check-in and invite friends to earn points
- 📊 **Admin Panel**: Complete admin features (blacklist, card keys, broadcast, etc.)
- 🐳 **Docker Deployment**: One-click deployment, ready to use

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Framework**: python-telegram-bot 20.0+
- **Database**: MySQL 5.7+
- **Browser Automation**: Playwright 1.48.0
- **HTTP Client**: httpx (async)
- **Image Processing**: Pillow, reportlab
- **Containerization**: Docker + Docker Compose

---

## 📦 Quick Start

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7+ (Recommended) or SQLite (Development/Testing)
- Telegram Bot Token

### 1. Clone Repository

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### 3. Configuration

Copy `env.example` to `.env` and fill in your configuration:

```bash
cp env.example .env
```

Edit `.env` file:

```bash
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel
ADMIN_USER_ID=123456789

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tgbot_user
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=tgbot_verify
```

**Or directly modify `config.py`** (Not recommended, may leak sensitive information)

### 4. Initialize Database

Database tables will be created automatically on first run.

### 5. Start the Bot

```bash
# Direct run
python bot.py

# Or using virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

---

## 🐳 Docker Deployment (Recommended)

### Using Docker Compose

1. **Configure Environment Variables**

Edit `docker-compose.yml`:

```yaml
environment:
  - MYSQL_HOST=your_mysql_host
  - MYSQL_PORT=3306
  - MYSQL_USER=your_user
  - MYSQL_PASSWORD=your_password
  - MYSQL_DATABASE=tgbot_verify
```

2. **Start Services**

```bash
docker-compose up -d
```

3. **View Logs**

```bash
docker-compose logs -f
```

4. **Stop Services**

```bash
docker-compose down
```

### Manual Docker Deployment

```bash
# Build image
docker build -t tgbot-verify .

# Run container
docker run -d \
  --name tgbot-verify \
  -e MYSQL_HOST=your_host \
  -e MYSQL_USER=your_user \
  -e MYSQL_PASSWORD=your_password \
  -e MYSQL_DATABASE=tgbot_verify \
  --restart unless-stopped \
  tgbot-verify
```

---

## 📖 User Guide

### User Commands

```
/start          - Register account (get 1 point)
/help           - View help
/balance        - Check points balance
/qd             - Daily check-in (+1 point)
/invite         - Invite friends (+2 points/person)
/use <key>      - Use card key to redeem points

/verify <link>  - Gemini One Pro verification
/verify2 <link> - ChatGPT Teacher K12 verification
/verify4 <link> - Bolt.new Teacher verification (Fully Auto)
/getV4Code <id> - Get Bolt.new verification code
```

### Admin Commands

```
/addbalance <user_id> <points>  - Add user points
/block <user_id>                - Block user
/white <user_id>                - Unblock user
/blacklist                      - View blacklist
/genkey <key> <points> [uses] [days] - Generate card key
/listkeys                       - View card keys
/broadcast <text>               - Broadcast message
```

### Usage Example

```
# 1. Register account
/start

# 2. Daily check-in for points
/qd

# 3. Start verification (Bolt.new example)
/verify4 https://services.sheerid.com/verify/xxx/?verificationId=xxx

# 4. Wait for automatic processing, bot will return verification code
```

---

## 🏗️ Project Structure

```
tgbot-verify/
├── bot.py                  # Main entry point
├── config.py               # Global configuration
├── database_mysql.py       # MySQL database implementation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
│
├── handlers/               # Command handlers
│   ├── user_commands.py    # User commands
│   ├── verify_commands.py  # Verification commands
│   └── admin_commands.py   # Admin commands
│
├── utils/                  # Utility modules
│   ├── checks.py           # Permission checks
│   ├── concurrency.py      # Concurrency control
│   └── messages.py         # Message templates
│
├── one/                    # Gemini One verification module
│   ├── sheerid_verifier.py
│   ├── img_generator.py
│   └── name_generator.py
│
├── k12/                    # K12 teacher verification module
│   ├── sheerid_verifier.py
│   ├── img_generator.py
│   └── name_generator.py
│
└── Boltnew/                # Bolt.new verification module
    ├── sheerid_verifier.py
    ├── img_generator.py
    └── name_generator.py
```

---

## ⚙️ Configuration Guide

### Points System Configuration

Edit `config.py`:

```python
VERIFY_COST = 1         # Points consumed per verification
CHECKIN_REWARD = 1      # Check-in reward points
INVITE_REWARD = 2       # Invitation reward points
REGISTER_REWARD = 1     # Registration reward points
```

### Concurrency Control

Edit `utils/concurrency.py` to adjust concurrency:

```python
_base_concurrency = 20  # Base concurrency (auto-calculated based on system resources)
```

---

## ⚠️ Important Notes

1. **Compliance**: This tool is for educational purposes only, please comply with platform terms of service
2. **Personal Use**: Code is an early version, suitable for personal use, needs optimization for commercial use
3. **Data Security**: Keep your Bot Token and database password safe
4. **Rate Limiting**: Set reasonable concurrency limits to avoid platform bans
5. **Regular Updates**: SheerID platform may update verification process, code needs timely adjustments

---

## 🤝 Community & Support

- **Telegram Channel**: [PK Personal Channel](https://t.me/pk_oa) - Project updates, tutorials
- **Telegram Group**: [Let's Communicate](https://t.me/pastking_server) - Technical exchange, feedback

---

## 🔧 Secondary Development

Welcome to develop based on this project, but please follow these rules:

1. ✅ **Keep Original Repository Link**: Preserve this repository address in your project
2. ✅ **Open Source Spirit**: Recommend keeping your modifications open source
3. ✅ **Attribution**: Indicate that the project is based on this repository

### Contributing

If you have suggestions for improvements:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open sourced under **MIT License**, see [LICENSE](LICENSE) file for details.

**Brief Description**:
- ✅ Free to use, modify, and distribute
- ✅ Can be used for commercial purposes (but please optimize yourself)
- ⚠️ Must retain copyright and license notices
- ⚠️ Software provided "as is" without any warranty

---

## 🙏 Acknowledgments

- Original bot: [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) (GGBond)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot framework
- [Playwright](https://playwright.dev/) - Browser automation tool
- [SheerID](https://www.sheerid.com/) - Identity verification platform

---

## 📊 Changelog

### v2.0.0 (Current Version)
- ✨ Migrated to MySQL database
- ✨ Support high concurrency
- ✨ Bolt.new fully automated verification
- ✨ Performance optimization (3-90x improvement)
- ❌ Removed Spotify verification module

### v1.0.0
- 🎉 Initial release

---

## 📞 Contact

- **GitHub**: [Submit Issue](https://github.com/PastKing/tgbot-verify/issues)
- **Telegram**: [@pk_oa](https://t.me/pk_oa)
- **Group**: [Let's Communicate](https://t.me/pastking_server)

---

<div align="center">

**⭐ If this project helps you, please give it a Star!**

Made with ❤️ by PK

[⬆ Back to Top](#sheerid-auto-verification-bot)

</div>

