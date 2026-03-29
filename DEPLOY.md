# SheerID 自动认证机器人 - 部署指南

[English](DEPLOY_EN.md) | 中文

本文档详细说明如何部署 SheerID 自动认证 Telegram 机器人。

---

## 📋 目录

1. [环境要求](#环境要求)
2. [快速部署](#快速部署)
3. [Docker 部署](#docker-部署)
4. [手动部署](#手动部署)
5. [配置说明](#配置说明)
6. [常见问题](#常见问题)
7. [维护和更新](#维护和更新)

---

## 🔧 环境要求

### 最低配置

- **操作系统**：Linux (Ubuntu 20.04+推荐) / Windows 10+ / macOS 10.15+
- **Python**：3.11 或更高版本
- **MySQL**：5.7 或更高版本
- **内存**：512MB RAM（推荐 1GB+）
- **磁盘空间**：2GB+
- **网络**：稳定的互联网连接

### 推荐配置

- **操作系统**：Ubuntu 22.04 LTS
- **Python**：3.11
- **MySQL**：8.0
- **内存**：2GB+ RAM
- **磁盘空间**：5GB+
- **网络**：带宽 10Mbps+

---

## 🚀 快速部署

### 使用 Docker Compose（最简单）

```bash
# 1. 克隆仓库
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify

# 2. 配置环境变量
cp env.example .env
nano .env  # 填写你的配置

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 停止服务
docker-compose down
```

完成！机器人应该已经运行了。

---

## 🐳 Docker 部署

### 方法 1：使用 Docker Compose（推荐）

#### 1. 准备配置文件

创建 `.env` 文件：

```env
# Telegram Bot 配置
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
CHANNEL_USERNAME=pk_oa
CHANNEL_URL=https://t.me/pk_oa
ADMIN_USER_ID=123456789

# MySQL 数据库配置
MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_USER=tgbot_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=tgbot_verify
```

#### 2. 启动服务

```bash
docker-compose up -d
```

#### 3. 查看状态

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 查看最近50行日志
docker-compose logs --tail=50
```

#### 4. 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启单个服务
docker-compose restart tgbot
```

#### 5. 更新代码

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

### 方法 2：手动 Docker 部署

```bash
# 1. 构建镜像
docker build -t tgbot-verify:latest .

# 2. 运行容器
docker run -d \
  --name tgbot-verify \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  tgbot-verify:latest

# 3. 查看日志
docker logs -f tgbot-verify

# 4. 停止容器
docker stop tgbot-verify

# 5. 删除容器
docker rm tgbot-verify
```

---

## 🔨 手动部署

### Linux / macOS

#### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv mysql-server

# macOS (使用 Homebrew)
brew install python@3.11 mysql
```

#### 2. 创建虚拟环境

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
```

#### 3. 安装 Python 包

```bash
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 4. 配置数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库和用户
CREATE DATABASE tgbot_verify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tgbot_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON tgbot_verify.* TO 'tgbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 5. 配置环境变量

```bash
cp env.example .env
nano .env  # 编辑配置
```

#### 6. 启动机器人

```bash
# 前台运行（测试）
python bot.py

# 后台运行（使用 nohup）
nohup python bot.py > bot.log 2>&1 &

# 后台运行（使用 screen）
screen -S tgbot
python bot.py
# Ctrl+A+D 退出 screen
# screen -r tgbot 重新连接
```

### Windows

#### 1. 安装依赖

- 下载并安装 [Python 3.11+](https://www.python.org/downloads/)
- 下载并安装 [MySQL](https://dev.mysql.com/downloads/installer/)

#### 2. 创建虚拟环境

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. 安装 Python 包

```cmd
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 4. 配置数据库

使用 MySQL Workbench 或命令行创建数据库。

#### 5. 配置环境变量

复制 `env.example` 为 `.env` 并编辑。

#### 6. 启动机器人

```cmd
python bot.py
```

---

## ⚙️ 配置说明

### 环境变量详解

#### Telegram 配置

```env
# Bot Token（必填）
# 从 @BotFather 获取
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# 频道用户名（选填）
# 不需要 @ 符号
CHANNEL_USERNAME=pk_oa

# 频道链接（选填）
CHANNEL_URL=https://t.me/pk_oa

# 管理员 Telegram ID（必填）
# 可以通过 @userinfobot 获取
ADMIN_USER_ID=123456789
```

#### MySQL 配置

```env
# 数据库主机（必填）
MYSQL_HOST=localhost         # 本地部署
# MYSQL_HOST=192.168.1.100  # 远程数据库
# MYSQL_HOST=mysql          # Docker Compose

# 数据库端口（选填，默认 3306）
MYSQL_PORT=3306

# 数据库用户名（必填）
MYSQL_USER=tgbot_user

# 数据库密码（必填）
MYSQL_PASSWORD=your_secure_password

# 数据库名称（必填）
MYSQL_DATABASE=tgbot_verify
```

### 积分系统配置

在 `config.py` 中修改：

```python
# 积分配置
VERIFY_COST = 1        # 验证消耗的积分
CHECKIN_REWARD = 1     # 签到奖励积分
INVITE_REWARD = 2      # 邀请奖励积分
REGISTER_REWARD = 1    # 注册奖励积分
```

### 并发控制

在 `utils/concurrency.py` 中调整：

```python
# 根据系统资源自动计算
_base_concurrency = _calculate_max_concurrency()

# 每种验证类型的并发限制
_verification_semaphores = {
    "gemini_one_pro": Semaphore(_base_concurrency // 5),
    "chatgpt_teacher_k12": Semaphore(_base_concurrency // 5),
    "spotify_student": Semaphore(_base_concurrency // 5),
    "youtube_student": Semaphore(_base_concurrency // 5),
    "bolt_teacher": Semaphore(_base_concurrency // 5),
}
```

---

## 🔍 常见问题

### 1. Bot Token 无效

**问题**：`telegram.error.InvalidToken: The token was rejected by the server.`

**解决方案**：
- 检查 `.env` 文件中的 `BOT_TOKEN` 是否正确
- 确保没有多余的空格或引号
- 从 @BotFather 重新获取 Token

### 2. 数据库连接失败

**问题**：`pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**解决方案**：
- 检查 MySQL 服务是否运行：`systemctl status mysql`
- 检查数据库配置是否正确
- 检查防火墙设置
- 确认数据库用户权限

### 3. Playwright 浏览器安装失败

**问题**：`playwright._impl._api_types.Error: Executable doesn't exist`

**解决方案**：
```bash
playwright install chromium
# 或者安装所有依赖
playwright install-deps chromium
```

### 4. 端口被占用

**问题**：Docker 容器无法启动，端口冲突

**解决方案**：
```bash
# 查看端口占用
netstat -tlnp | grep :3306
# 修改 docker-compose.yml 中的端口映射
```

### 5. 内存不足

**问题**：服务器内存不足导致崩溃

**解决方案**：
- 增加服务器内存
- 减少并发数量
- 启用 swap 交换空间：
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 6. 日志文件过大

**问题**：日志文件占用大量磁盘空间

**解决方案**：
- Docker 自动限制日志大小（见 `docker-compose.yml`）
- 手动清理：`truncate -s 0 logs/*.log`
- 设置日志轮转

---

## 🔄 维护和更新

### 查看日志

```bash
# Docker Compose
docker-compose logs -f --tail=100

# 手动部署
tail -f bot.log
tail -f logs/bot.log
```

### 备份数据库

```bash
# 完整备份
mysqldump -u tgbot_user -p tgbot_verify > backup_$(date +%Y%m%d).sql

# 只备份数据
mysqldump -u tgbot_user -p --no-create-info tgbot_verify > data_backup.sql

# 恢复备份
mysql -u tgbot_user -p tgbot_verify < backup.sql
```

### 更新代码

```bash
# 拉取最新代码
git pull origin main

# Docker 部署
docker-compose down
docker-compose up -d --build

# 手动部署
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

### 监控运行状态

#### 使用 systemd（Linux 推荐）

创建服务文件 `/etc/systemd/system/tgbot-verify.service`：

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

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable tgbot-verify
sudo systemctl start tgbot-verify
sudo systemctl status tgbot-verify
```

#### 使用 supervisor

安装 supervisor：

```bash
sudo apt install supervisor
```

创建配置文件 `/etc/supervisor/conf.d/tgbot-verify.conf`：

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

启动：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tgbot-verify
```

---

## 🔒 安全建议

1. **使用强密码**
   - Bot Token 定期轮换
   - 数据库密码至少 16 位
   - 不要使用默认密码

2. **限制数据库访问**
   ```sql
   # 只允许本地连接
   CREATE USER 'tgbot_user'@'localhost' IDENTIFIED BY 'password';
   
   # 允许特定 IP
   CREATE USER 'tgbot_user'@'192.168.1.100' IDENTIFIED BY 'password';
   ```

3. **配置防火墙**
   ```bash
   # 只开放必要端口
   sudo ufw allow 22/tcp      # SSH
   sudo ufw enable
   ```

4. **定期更新**
   ```bash
   sudo apt update && sudo apt upgrade
   pip install --upgrade -r requirements.txt
   ```

5. **备份策略**
   - 每天自动备份数据库
   - 保留至少 7 天的备份
   - 定期测试恢复流程

---

## 📞 技术支持

- 📺 Telegram 频道：https://t.me/pk_oa
- 🐛 问题反馈：[GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

---

<p align="center">
  <strong>祝您部署顺利！</strong>
</p>
