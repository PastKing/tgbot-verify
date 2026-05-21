"""Cấu hình toàn cục"""
import os
from dotenv import load_dotenv

# Nạp file .env
load_dotenv()

# Cấu hình Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "pk_oa")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/pk_oa")

# Cấu hình quản trị viên
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))

# Cấu hình điểm
VERIFY_COST = 1  # Điểm tiêu hao cho mỗi lần xác thực
CHECKIN_REWARD = 1  # Điểm thưởng khi điểm danh
INVITE_REWARD = 2  # Điểm thưởng khi mời bạn bè
REGISTER_REWARD = 1  # Điểm thưởng khi đăng ký

# Liên kết hướng dẫn
HELP_NOTION_URL = "https://rhetorical-era-3f3.notion.site/dd78531dbac745af9bbac156b51da9cc"
