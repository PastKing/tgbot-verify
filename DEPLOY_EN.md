# SheerID Auto-Verification Bot - Deployment Guide

[中文](DEPLOY.md) | English

This document provides detailed instructions on how to deploy the SheerID Auto-Verification Telegram Bot.

---

## 📋 Table of Contents

1. [Requirements](#requirements)
2. [Quick Deployment](#quick-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Manual Deployment](#manual-deployment)
5. [Configuration](#configuration)
6. [FAQ](#faq)
7. [Maintenance & Updates](#maintenance--updates)

---

## 🔧 Requirements

### Minimum

- **OS**: Linux (Ubuntu 20.04+ recommended) / Windows 10+ / macOS 10.15+
- **Python**: 3.11 or higher
- **MySQL**: 5.7 or higher
- **Memory**: 512 MB RAM (1 GB+ recommended)
- **Disk**: 2 GB+
- **Network**: Stable internet connection

### Recommended

- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.11
- **MySQL**: 8.0
- **Memory**: 2 GB+ RAM
- **Disk**: 5 GB+
- **Network**: 10 Mbps+ bandwidth

---

## 🚀 Quick Deployment

### Using Docker Compose (Easiest)

```bash
# 1. Clone the repository
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify

# 2. Configure environment variables
cp env.example .env
nano .env  # Fill in your configuration

# 3. Start the service
docker-compose up -d

# 4. View logs
docker-compose logs -f

# 5. Stop the service
docker-compose down
```

Done! The bot should now be running.

---

## 🐳 Docker Deployment

### Method 1: Docker Compose (Recommended)

#### 1. Prepare Configuration

Create the `.env` file:

```env
# Telegram Bot Configuration
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
CHANNEL_USERNAME=pk_oa
CHANNEL_URL=https://t.me/pk_oa
ADMIN_USER_ID=123456789

# MySQL Database Configuration
MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_USER=tgbot_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=tgbot_verify
```

#### 2. Start the Service

```bash
docker-compose up -d
```

#### 3. Check Status

```bash
# View container status
docker-compose ps

# View real-time logs
docker-compose logs -f

# View last 50 lines of logs
docker-compose logs --tail=50
```

#### 4. Restart the Service

```bash
# Restart all services
docker-compose restart

# Restart a specific service
docker-compose restart tgbot
```

#### 5. Update Code

```bash
# Pull the latest code
git pull

# Rebuild and start
docker-compose up -d --build
```

### Method 2: Manual Docker Deployment

```bash
# 1. Build the image
docker build -t tgbot-verify:latest .

# 2. Run the container
docker run -d \
  --name tgbot-verify \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  tgbot-verify:latest

# 3. View logs
docker logs -f tgbot-verify

# 4. Stop the container
docker stop tgbot-verify

# 5. Remove the container
docker rm tgbot-verify
```

---

## 🔨 Manual Deployment

### Linux / macOS

#### 1. Install Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv mysql-server

# macOS (using Homebrew)
brew install python@3.11 mysql
```

#### 2. Create a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
```

#### 3. Install Python Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 4. Set Up the Database

```bash
# Log in to MySQL
mysql -u root -p

# Create the database and user
CREATE DATABASE tgbot_verify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tgbot_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON tgbot_verify.* TO 'tgbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 5. Configure Environment Variables

```bash
cp env.example .env
nano .env  # Edit configuration
```

#### 6. Start the Bot

```bash
# Foreground (for testing)
python bot.py

# Background (using nohup)
nohup python bot.py > bot.log 2>&1 &

# Background (using screen)
screen -S tgbot
python bot.py
# Press Ctrl+A+D to detach
# Run `screen -r tgbot` to reattach
```

### Windows

#### 1. Install Dependencies

- Download and install [Python 3.11+](https://www.python.org/downloads/)
- Download and install [MySQL](https://dev.mysql.com/downloads/installer/)

#### 2. Create a Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Python Packages

```cmd
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 4. Set Up the Database

Create the database using MySQL Workbench or the command line.

#### 5. Configure Environment Variables

Copy `env.example` to `.env` and edit it.

#### 6. Start the Bot

```cmd
python bot.py
```

---

## ⚙️ Configuration

### Environment Variables

#### Telegram Settings

```env
# Bot Token (required)
# Obtain from @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Channel username (optional)
# Without the @ symbol
CHANNEL_USERNAME=pk_oa

# Channel URL (optional)
CHANNEL_URL=https://t.me/pk_oa

# Admin Telegram ID (required)
# Get yours via @userinfobot
ADMIN_USER_ID=123456789
```

#### MySQL Settings

```env
# Database host (required)
MYSQL_HOST=localhost         # Local deployment
# MYSQL_HOST=192.168.1.100  # Remote database
# MYSQL_HOST=mysql           # Docker Compose

# Database port (optional, default 3306)
MYSQL_PORT=3306

# Database username (required)
MYSQL_USER=tgbot_user

# Database password (required)
MYSQL_PASSWORD=your_secure_password

# Database name (required)
MYSQL_DATABASE=tgbot_verify
```

### Points System

Modify in `config.py`:

```python
VERIFY_COST = 1        # Points consumed per verification
CHECKIN_REWARD = 1     # Daily check-in reward
INVITE_REWARD = 2      # Invitation reward
REGISTER_REWARD = 1    # Registration reward
```

### Concurrency Control

Adjust in `utils/concurrency.py`:

```python
# Automatically calculated based on system resources
_base_concurrency = _calculate_max_concurrency()

# Concurrency limit per verification type
_verification_semaphores = {
    "gemini_one_pro": Semaphore(_base_concurrency // 5),
    "chatgpt_teacher_k12": Semaphore(_base_concurrency // 5),
    "spotify_student": Semaphore(_base_concurrency // 5),
    "youtube_student": Semaphore(_base_concurrency // 5),
    "bolt_teacher": Semaphore(_base_concurrency // 5),
}
```

---

## 🔍 FAQ

### 1. Invalid Bot Token

**Error**: `telegram.error.InvalidToken: The token was rejected by the server.`

**Solution**:
- Verify the `BOT_TOKEN` in your `.env` file is correct
- Make sure there are no extra spaces or quotes
- Regenerate the token from @BotFather

### 2. Database Connection Failed

**Error**: `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**Solution**:
- Check if MySQL is running: `systemctl status mysql`
- Verify your database configuration
- Check firewall settings
- Confirm database user permissions

### 3. Playwright Browser Installation Failed

**Error**: `playwright._impl._api_types.Error: Executable doesn't exist`

**Solution**:
```bash
playwright install chromium
# Or install all dependencies
playwright install-deps chromium
```

### 4. Port Already in Use

**Error**: Docker container fails to start due to port conflict

**Solution**:
```bash
# Check which process occupies the port
netstat -tlnp | grep :3306
# Change the port mapping in docker-compose.yml
```

### 5. Out of Memory

**Error**: Server crashes due to insufficient memory

**Solution**:
- Increase server memory
- Reduce concurrency limits
- Enable swap space:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 6. Log Files Too Large

**Error**: Log files consume excessive disk space

**Solution**:
- Docker automatically limits log size (see `docker-compose.yml`)
- Manual cleanup: `truncate -s 0 logs/*.log`
- Set up log rotation

---

## 🔄 Maintenance & Updates

### Viewing Logs

```bash
# Docker Compose
docker-compose logs -f --tail=100

# Manual deployment
tail -f bot.log
tail -f logs/bot.log
```

### Database Backup

```bash
# Full backup
mysqldump -u tgbot_user -p tgbot_verify > backup_$(date +%Y%m%d).sql

# Data only backup
mysqldump -u tgbot_user -p --no-create-info tgbot_verify > data_backup.sql

# Restore from backup
mysql -u tgbot_user -p tgbot_verify < backup.sql
```

### Updating Code

```bash
# Pull the latest code
git pull origin main

# Docker deployment
docker-compose down
docker-compose up -d --build

# Manual deployment
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

### Monitoring

#### Using systemd (Recommended for Linux)

Create a service file at `/etc/systemd/system/tgbot-verify.service`:

```ini
[Unit]
Description=SheerID Telegram Verification Bot
After=network.target mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/tgbot-verify
ExecStart=/path/to/tgbot-verify/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tgbot-verify
sudo systemctl start tgbot-verify
sudo systemctl status tgbot-verify
```

#### Using Supervisor

Install Supervisor:

```bash
sudo apt install supervisor
```

Create a config file at `/etc/supervisor/conf.d/tgbot-verify.conf`:

```ini
[program:tgbot-verify]
directory=/path/to/tgbot-verify
command=/path/to/tgbot-verify/venv/bin/python bot.py
autostart=true
autorestart=true
stderr_logfile=/var/log/tgbot-verify.err.log
stdout_logfile=/var/log/tgbot-verify.out.log
user=ubuntu
```

Start:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tgbot-verify
```

---

## 🔒 Security Recommendations

1. **Use Strong Passwords**
   - Rotate Bot Token periodically
   - Use database passwords of at least 16 characters
   - Never use default passwords

2. **Restrict Database Access**
   ```sql
   -- Allow local connections only
   CREATE USER 'tgbot_user'@'localhost' IDENTIFIED BY 'password';
   
   -- Allow a specific IP
   CREATE USER 'tgbot_user'@'192.168.1.100' IDENTIFIED BY 'password';
   ```

3. **Configure Firewall**
   ```bash
   # Only open necessary ports
   sudo ufw allow 22/tcp      # SSH
   sudo ufw enable
   ```

4. **Keep Software Updated**
   ```bash
   sudo apt update && sudo apt upgrade
   pip install --upgrade -r requirements.txt
   ```

5. **Backup Strategy**
   - Automate daily database backups
   - Retain at least 7 days of backups
   - Regularly test the restore process

---

## 📞 Support

- 📺 Telegram Channel: https://t.me/pk_oa
- 🐛 Bug Reports: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

---

<p align="center">
  <strong>Happy deploying!</strong>
</p>
