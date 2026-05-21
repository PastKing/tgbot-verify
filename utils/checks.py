"""Công cụ kiểm tra quyền và xác thực"""
import logging
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from config import CHANNEL_USERNAME

logger = logging.getLogger(__name__)


def is_group_chat(update: Update) -> bool:
    """Kiểm tra có phải chat nhóm hay không"""
    chat = update.effective_chat
    return chat and chat.type in ("group", "supergroup")


async def reject_group_command(update: Update) -> bool:
    """Giới hạn trong nhóm: chỉ cho phép /verify /verify2 /verify3 /verify4 /verify5 /qd"""
    if is_group_chat(update):
        await update.message.reply_text("Trong nhóm chỉ hỗ trợ /verify /verify2 /verify3 /verify4 /verify5 /qd, vui lòng dùng riêng tư cho các lệnh khác.")
        return True
    return False


async def check_channel_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Kiểm tra người dùng đã tham gia kênh hay chưa"""
    try:
        member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramError as e:
        logger.error("Kiểm tra thành viên kênh thất bại: %s", e)
        return False
