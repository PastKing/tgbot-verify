# SheerID 自动认证机器人

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Telegram](https://img.shields.io/badge/telegram-bot-blue)

**一个自动化的 Telegram 机器人，用于完成 SheerID 学生/教师身份认证**

[English](./README_EN.md) | 简体中文

</div>

---

## 📢 重要声明

> 本项目为 [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) (GGBond) 的**早期版本代码**  
> **个人使用足够，商业使用请自行优化**  
> 仅供学习交流使用，请勿用于非法用途

---

## ✨ 项目简介

这是一个基于 Python Telegram Bot 的自动化认证工具，能够自动完成 SheerID 平台的学生/教师身份验证流程。通过模拟真实用户操作，自动生成并提交认证文档，大大简化了认证过程。

### 🎯 支持的认证服务

| 服务 | 命令 | 说明 |
|------|------|------|
| ✅ Gemini One Pro | `/verify` | Google Gemini 学生认证 |
| ✅ ChatGPT Teacher K12 | `/verify2` | OpenAI 教师认证 |
| ✅ Bolt.new Teacher | `/verify4` | Bolt.new 教师认证（全自动） |
| ❌ ~~Spotify Student~~ | ~~`/verify3`~~ | **已移除** |

> **注意**: Spotify 认证模块已从本版本中移除

---

## 🚀 核心特性

- 🤖 **全自动流程**: 一键提交，自动生成文档并完成认证
- ⚡ **高并发支持**: 支持多用户同时使用，互不干扰
- 💾 **MySQL 数据库**: 企业级数据存储，支持大规模用户
- 🎨 **智能文档生成**: 使用 Playwright 渲染高质量认证文档
- 🔐 **积分系统**: 签到、邀请好友获取积分
- 📊 **管理后台**: 完善的管理员功能（黑名单、卡密、广播等）
- 🐳 **Docker 部署**: 一键部署，开箱即用

---

## 🛠️ 技术栈

- **语言**: Python 3.8+
- **框架**: python-telegram-bot 20.0+
- **数据库**: MySQL 5.7+
- **浏览器自动化**: Playwright 1.48.0
- **HTTP 客户端**: httpx (异步)
- **图片处理**: Pillow, reportlab
- **容器化**: Docker + Docker Compose

---

## 📦 快速开始

### 前置要求

- Python 3.8 或更高版本
- MySQL 5.7+ （推荐）或 SQLite（开发测试）
- Telegram Bot Token

### 1. 克隆仓库

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. 安装依赖

```bash
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 3. 配置环境

复制 `env.example` 为 `.env` 并填写配置：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```bash
# Telegram Bot 配置
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel
ADMIN_USER_ID=123456789

# MySQL 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tgbot_user
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=tgbot_verify
```

**或者直接修改 `config.py`** (不推荐，容易泄露敏感信息)

### 4. 初始化数据库

程序首次运行时会自动创建数据库表结构。

### 5. 启动机器人

```bash
# 直接运行
python bot.py

# 或使用虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

---

## 🐳 Docker 部署 (推荐)

### 使用 Docker Compose

1. **配置环境变量**

编辑 `docker-compose.yml`:

```yaml
environment:
  - MYSQL_HOST=your_mysql_host
  - MYSQL_PORT=3306
  - MYSQL_USER=your_user
  - MYSQL_PASSWORD=your_password
  - MYSQL_DATABASE=tgbot_verify
```

2. **启动服务**

```bash
docker-compose up -d
```

3. **查看日志**

```bash
docker-compose logs -f
```

4. **停止服务**

```bash
docker-compose down
```

### 手动 Docker 部署

```bash
# 构建镜像
docker build -t tgbot-verify .

# 运行容器
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

## 📖 使用指南

### 用户命令

```
/start          - 注册账号（赠送 1 积分）
/help           - 查看帮助
/balance        - 查看积分余额
/qd             - 每日签到（+1 积分）
/invite         - 邀请好友（+2 积分/人）
/use <卡密>     - 使用卡密兑换积分

/verify <链接>  - Gemini One Pro 认证
/verify2 <链接> - ChatGPT Teacher K12 认证
/verify4 <链接> - Bolt.new Teacher 认证（全自动）
/getV4Code <id> - 获取 Bolt.new 认证码
```

### 管理员命令

```
/addbalance <用户ID> <积分>  - 增加用户积分
/block <用户ID>              - 拉黑用户
/white <用户ID>              - 取消拉黑
/blacklist                   - 查看黑名单
/genkey <卡密> <积分> [次数] [天数] - 生成卡密
/listkeys                    - 查看卡密列表
/broadcast <文本>            - 群发消息
```

### 使用示例

```
# 1. 注册账号
/start

# 2. 签到获取积分
/qd

# 3. 开始认证（以 Bolt.new 为例）
/verify4 https://services.sheerid.com/verify/xxx/?verificationId=xxx

# 4. 等待自动处理，机器人会返回认证码
```

---

## 🏗️ 项目结构

```
tgbot-verify/
├── bot.py                  # 主程序入口
├── config.py               # 全局配置
├── database_mysql.py       # MySQL 数据库实现
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 镜像配置
├── docker-compose.yml      # Docker Compose 配置
│
├── handlers/               # 命令处理器
│   ├── user_commands.py    # 用户命令
│   ├── verify_commands.py  # 认证命令
│   └── admin_commands.py   # 管理员命令
│
├── utils/                  # 工具模块
│   ├── checks.py           # 权限检查
│   ├── concurrency.py      # 并发控制
│   └── messages.py         # 消息模板
│
├── one/                    # Gemini One 认证模块
│   ├── sheerid_verifier.py
│   ├── img_generator.py
│   └── name_generator.py
│
├── k12/                    # K12 教师认证模块
│   ├── sheerid_verifier.py
│   ├── img_generator.py
│   └── name_generator.py
│
└── Boltnew/                # Bolt.new 认证模块
    ├── sheerid_verifier.py
    ├── img_generator.py
    └── name_generator.py
```

---

## ⚙️ 配置说明

### 积分系统配置

编辑 `config.py`:

```python
VERIFY_COST = 1         # 每次认证消耗积分
CHECKIN_REWARD = 1      # 签到奖励积分
INVITE_REWARD = 2       # 邀请奖励积分
REGISTER_REWARD = 1     # 注册奖励积分
```

### 并发控制

编辑 `utils/concurrency.py` 调整并发数量：

```python
_base_concurrency = 20  # 基础并发数（自动根据系统资源计算）
```

---

## ⚠️ 注意事项

1. **合规使用**: 本工具仅供学习研究，请遵守相关平台的服务条款
2. **个人使用**: 代码为早期版本，适合个人使用，商业场景需自行优化
3. **数据安全**: 请妥善保管 Bot Token 和数据库密码
4. **频率限制**: 建议设置合理的并发限制，避免被平台封禁
5. **定期更新**: SheerID 平台可能更新验证流程，需要及时调整代码

---

## 🤝 社区与支持

- **Telegram 频道**: [PK个人频道](https://t.me/pk_oa) - 项目更新、教程分享
- **Telegram 群组**: [我们来交流](https://t.me/pastking_server) - 技术交流、问题反馈

---

## 🔧 二次开发

欢迎基于本项目进行二次开发，但请遵守以下规则：

1. ✅ **保留原仓库链接**: 在您的项目中保留本仓库地址
2. ✅ **开源精神**: 建议您的修改也保持开源
3. ✅ **署名说明**: 说明项目基于本仓库开发

### 贡献代码

如果您有改进建议：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

---

## 📄 开源协议

本项目基于 **MIT License** 开源，详见 [LICENSE](LICENSE) 文件。

**简要说明**:
- ✅ 可以自由使用、修改、分发
- ✅ 可以用于商业用途（但请自行优化）
- ⚠️ 需保留版权声明和许可声明
- ⚠️ 软件按"原样"提供，不提供任何保证

---

## 🙏 致谢

- 原始机器人: [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) (GGBond)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot 框架
- [Playwright](https://playwright.dev/) - 浏览器自动化工具
- [SheerID](https://www.sheerid.com/) - 身份验证平台

---

## 📊 更新日志

### v2.0.0 (当前版本)
- ✨ 迁移到 MySQL 数据库
- ✨ 支持高并发处理
- ✨ Bolt.new 全自动认证
- ✨ 优化性能（3-90倍提升）
- ❌ 移除 Spotify 认证模块

### v1.0.0
- 🎉 初始版本发布

---

## 📞 联系方式

- **GitHub**: [提交 Issue](https://github.com/PastKing/tgbot-verify/issues)
- **Telegram**: [@pk_oa](https://t.me/pk_oa)
- **群组**: [我们来交流](https://t.me/pastking_server)

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给个 Star！**

Made with ❤️ by PK

[⬆ 回到顶部](#sheerid-自动认证机器人)

</div>
