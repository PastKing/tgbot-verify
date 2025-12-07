# 部署指南

## 🚀 快速部署

### 方式一：使用 Docker Compose（推荐）

1. **克隆仓库**
```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

2. **配置环境变量**
```bash
cp env.example .env
# 编辑 .env 文件，填写你的配置
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **查看日志**
```bash
docker-compose logs -f
```

### 方式二：直接运行

1. **安装依赖**
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **配置环境**
```bash
cp env.example .env
# 编辑 .env 文件
```

3. **运行机器人**
```bash
python bot.py
```

---

## 🔧 配置说明

### 必需配置

在 `.env` 文件中配置以下内容：

```bash
# 1. Telegram Bot Token（必须）
BOT_TOKEN=从 @BotFather 获取

# 2. 管理员 ID（必须）
ADMIN_USER_ID=你的 Telegram User ID

# 3. MySQL 数据库（必须）
MYSQL_HOST=数据库地址
MYSQL_USER=数据库用户名
MYSQL_PASSWORD=数据库密码
MYSQL_DATABASE=数据库名称
```

### 可选配置

```bash
# 频道设置
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel

# 积分设置（已有默认值）
VERIFY_COST=1
CHECKIN_REWARD=1
INVITE_REWARD=2
```

---

## 🐳 Docker 部署详解

### 环境变量方式（推荐）

创建 `.env` 文件后直接运行：

```bash
docker-compose up -d
```

Docker Compose 会自动读取 `.env` 文件中的变量。

### 命令行方式

```bash
docker run -d \
  --name tgbot-verify \
  -e BOT_TOKEN=your_token \
  -e ADMIN_USER_ID=123456 \
  -e MYSQL_HOST=your_host \
  -e MYSQL_USER=your_user \
  -e MYSQL_PASSWORD=your_password \
  -e MYSQL_DATABASE=tgbot_verify \
  --restart unless-stopped \
  tgbot-verify
```

---

## 📊 数据库初始化

数据库表会在首次运行时自动创建，无需手动初始化。

如果需要手动创建数据库：

```sql
CREATE DATABASE tgbot_verify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 🔍 故障排查

### 1. 机器人无响应

检查 Bot Token 是否正确：
```bash
docker-compose logs | grep "Bot Token"
```

### 2. 数据库连接失败

检查数据库配置和网络：
```bash
# 测试数据库连接
mysql -h HOST -u USER -p DATABASE
```

### 3. Playwright 错误

重新安装浏览器：
```bash
playwright install chromium
```

### 4. 查看完整日志

```bash
docker-compose logs -f --tail=100
```

---

## 🔄 更新部署

```bash
# 拉取最新代码
git pull

# 重启服务
docker-compose down
docker-compose up -d --build
```

---

## 📞 获取帮助

- GitHub Issues: https://github.com/PastKing/tgbot-verify/issues
- Telegram 频道: https://t.me/pk_oa
- Telegram 群组: https://t.me/pastking_server

