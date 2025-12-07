"""权限检查和验证工具"""
import logging
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from config import CHANNEL_USERNAME

logger = logging.getLogger(__name__)


def is_group_chat(update: Update) -> bool:
    """判断是否为群聊"""
    chat = update.effective_chat
    return chat and chat.type in ("group", "supergroup")


async def reject_group_command(update: Update) -> bool:
    """群聊限制：仅允许 /verify /verify2 /verify4 /qd"""
    if is_group_chat(update):
        await update.message.reply_text("群聊仅支持 /verify /verify2 /verify4 /qd，请私聊使用其他命令。")
        return True
    return False


async def check_channel_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """检查用户是否加入了频道"""
    try:
        member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramError as e:
        logger.error("检查频道成员失败: %s", e)
        return False
