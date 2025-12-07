"""全局配置文件"""
import os

# Telegram Bot 配置
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "pk_oa")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/pk_oa")

# 管理员配置
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))

# 积分配置
VERIFY_COST = 1  # 验证消耗的积分
CHECKIN_REWARD = 1  # 签到奖励积分
INVITE_REWARD = 2  # 邀请奖励积分
REGISTER_REWARD = 1  # 注册奖励积分

# 帮助链接
HELP_NOTION_URL = "https://rhetorical-era-3f3.notion.site/dd78531dbac745af9bbac156b51da9cc"
