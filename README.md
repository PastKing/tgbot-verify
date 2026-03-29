# SheerID 自动认证 Telegram 机器人

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> 🤖 自动完成 SheerID 学生/教师认证的 Telegram 机器人
>
> 基于 [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond 的旧版代码改进

[English](README_EN.md) | [繁體中文](README_TW.md) | 简体中文

---

## 📋 项目简介

基于 Python 的 Telegram 机器人，自动完成多个平台的 SheerID 学生/教师身份认证。机器人自动生成身份信息、创建认证文档并提交到 SheerID 平台，大幅简化认证流程。

### 🎯 支持的认证服务

| 命令 | 服务 | 类型 | 状态 |
|------|------|------|------|
| `/verify` | Gemini One Pro | 教师认证 | ✅ 完整 |
| `/verify2` | ChatGPT Teacher K12 | 教师认证 | ✅ 完整 |
| `/verify3` | Spotify Student | 学生认证 | ✅ 完整 |
| `/verify4` | Bolt.new Teacher | 教师认证 | ✅ 完整 |
| `/verify5` | YouTube Premium Student | 学生认证 | ⚠️ 开发中 |

> **⚠️ 使用前必读**：各模块的 `programId` 可能定期更新，使用前请检查并更新对应模块的 `config.py` 配置，详见下方"配置说明"章节。

### ✨ 核心功能

- 🚀 **自动化流程**：一键完成信息生成、文档创建、认证提交
- 🎨 **智能生成**：自动生成学生证/教师证 PNG 图片
- 💰 **积分系统**：签到、邀请、卡密兑换等多种获取方式
- 🔐 **安全可靠**：MySQL 数据库，支持环境变量配置
- ⚡ **并发控制**：智能管理并发请求，确保稳定性
- 👥 **管理功能**：完善的用户管理和积分管理系统

---

## 🛠️ 技术栈

- **语言**：Python 3.11+
- **Bot框架**：python-telegram-bot 20.0+
- **数据库**：MySQL 5.7+
- **浏览器自动化**：Playwright
- **HTTP客户端**：httpx
- **图像处理**：Pillow, reportlab, xhtml2pdf
- **环境管理**：python-dotenv

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. 配置环境变量

复制 `env.example` 为 `.env` 并填写配置：

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

### 4. 启动机器人

```bash
python bot.py
```

---

## 🐳 Docker 部署

```bash
cp env.example .env
nano .env
docker-compose up -d
docker-compose logs -f
```

手动构建：

```bash
docker build -t tgbot-verify .
docker run -d --name tgbot-verify --env-file .env -v $(pwd)/logs:/app/logs tgbot-verify
```

---

## 📖 使用说明

### 用户命令

```
/start              # 开始使用（注册）
/about              # 了解机器人功能
/balance            # 查看积分余额
/qd                 # 每日签到（+1积分）
/invite             # 生成邀请链接（+2积分/人）
/use <卡密>         # 使用卡密兑换积分
/verify <链接>      # Gemini One Pro 认证
/verify2 <链接>     # ChatGPT Teacher K12 认证
/verify3 <链接>     # Spotify Student 认证
/verify4 <链接>     # Bolt.new Teacher 认证
/verify5 <链接>     # YouTube Premium Student 认证
/help               # 查看帮助信息
```

### 管理员命令

```
/addbalance <用户ID> <积分>               # 增加用户积分
/block <用户ID>                           # 拉黑用户
/white <用户ID>                           # 取消拉黑
/blacklist                                # 查看黑名单
/genkey <卡密> <积分> [次数] [天数]       # 生成卡密
/listkeys                                 # 查看卡密列表
/broadcast <文本>                         # 群发通知
```

### 使用流程

1. 访问对应服务的认证页面，开始认证流程
2. 复制浏览器地址栏中包含 `verificationId` 的完整 URL
3. 发送给机器人：`/verify3 https://services.sheerid.com/verify/xxx/?verificationId=yyy`
4. 等待机器人自动处理，审核通常在几分钟内完成

---

## 📁 项目结构

```
tgbot-verify/
├── bot.py                  # 机器人主程序
├── config.py               # 全局配置
├── database_mysql.py       # MySQL 数据库管理
├── env.example             # 环境变量模板
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # Docker Compose 配置
├── handlers/               # 命令处理器
│   ├── user_commands.py
│   ├── admin_commands.py
│   └── verify_commands.py
├── one/                    # Gemini One Pro 模块
├── k12/                    # ChatGPT K12 模块
├── spotify/                # Spotify Student 模块
├── youtube/                # YouTube Premium 模块
├── Boltnew/                # Bolt.new 模块
├── military/               # ChatGPT 军人认证文档
└── utils/                  # 工具函数
    ├── messages.py
    ├── concurrency.py
    └── checks.py
```

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `BOT_TOKEN` | ✅ | Telegram Bot Token |
| `ADMIN_USER_ID` | ✅ | 管理员 Telegram ID |
| `MYSQL_HOST` | ✅ | MySQL 主机地址 |
| `MYSQL_USER` | ✅ | MySQL 用户名 |
| `MYSQL_PASSWORD` | ✅ | MySQL 密码 |
| `MYSQL_DATABASE` | ✅ | 数据库名称 |
| `CHANNEL_USERNAME` | ❌ | 频道用户名（默认 pk_oa）|
| `CHANNEL_URL` | ❌ | 频道链接 |
| `MYSQL_PORT` | ❌ | MySQL 端口（默认 3306）|

### 更新 programId

如果认证持续失败，通常是 `programId` 已过期。更新步骤：

1. 访问对应服务认证页面，打开浏览器开发者工具（F12）→ 网络标签
2. 开始认证流程，查找 `https://services.sheerid.com/rest/v2/verification/` 请求
3. 从请求中提取 `programId`，更新对应模块的 `config.py` 文件

需要更新的文件：`one/config.py` | `k12/config.py` | `spotify/config.py` | `youtube/config.py` | `Boltnew/config.py`

### 积分配置（config.py）

```python
VERIFY_COST = 1        # 验证消耗积分
CHECKIN_REWARD = 1     # 签到奖励
INVITE_REWARD = 2      # 邀请奖励
REGISTER_REWARD = 1    # 注册奖励
```

---

## 🤝 联系与合作

- 📢 **Telegram 频道**：[@pk_oa](https://t.me/pk_oa)
- 📧 **邮箱**：pastking69@gmail.com
- 🐛 **问题反馈**：[GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

欢迎合作与交流，有意向请通过以上方式联系。

---

## 🛠️ 二次开发

欢迎基于本项目进行二次开发，请遵守以下规则：

- 保留原仓库地址及作者信息
- 遵循 MIT 开源协议，二次开发项目须同样开源
- 个人使用免费；商业使用请自行优化并承担相应责任

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

- 感谢 [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond 提供的旧版代码基础
- 感谢所有为本项目做出贡献的开发者

---

## 📊 项目统计

[![Star History Chart](https://api.star-history.com/svg?repos=PastKing/tgbot-verify&type=Date)](https://star-history.com/#PastKing/tgbot-verify&Date)

---

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/PastKing">PastKing</a>
</p>
