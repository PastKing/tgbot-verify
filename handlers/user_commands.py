"""Bộ xử lý lệnh người dùng"""
import logging
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command
from utils.messages import (
    get_welcome_message,
    get_about_message,
    get_help_message,
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /start"""
    if await reject_group_command(update):
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    full_name = user.full_name or ""

    # Nếu đã khởi tạo thì trả về ngay
    if db.user_exists(user_id):
        await update.message.reply_text(
            f"Chào mừng trở lại, {full_name}!\n"
            "Bạn đã được khởi tạo rồi.\n"
            "Gửi /help để xem các lệnh khả dụng."
        )
        return

    # Mã mời
    invited_by: Optional[int] = None
    if context.args:
        try:
            invited_by = int(context.args[0])
            if not db.user_exists(invited_by):
                invited_by = None
        except Exception:
            invited_by = None

    # Tạo người dùng
    if db.create_user(user_id, username, full_name, invited_by):
        welcome_msg = get_welcome_message(full_name, bool(invited_by))
        await update.message.reply_text(welcome_msg)
    else:
        await update.message.reply_text("Đăng ký thất bại, vui lòng thử lại sau.")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /about"""
    if await reject_group_command(update):
        return

    await update.message.reply_text(get_about_message())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /help"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    is_admin = user_id == ADMIN_USER_ID
    await update.message.reply_text(get_help_message(is_admin))


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /balance"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Bạn đã bị chặn, không thể sử dụng tính năng này.")
        return

    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("Vui lòng dùng /start để đăng ký trước.")
        return

    await update.message.reply_text(
        f"💰 Số dư điểm\n\nĐiểm hiện tại: {user['balance']} điểm"
    )


async def checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /qd - tạm thời vô hiệu hóa"""
    user_id = update.effective_user.id

    # Tạm thời tắt tính năng điểm danh (đang bảo trì)
    # await update.message.reply_text(
    #     "⚠️ Tính năng điểm danh tạm thời đang bảo trì\n\n"
    #     "Do phát hiện lỗi, chức năng điểm danh đã tạm ngưng để sửa chữa.\n"
    #     "Sẽ sớm được khôi phục. Xin lỗi vì sự bất tiện.\n\n"
    #     "💡 Bạn có thể nhận điểm bằng cách:\n"
    #     "• Mời bạn bè /invite（+2 điểm）\n"
    #     "• Sử dụng mã nạp /use <mã>"
    # )
    # return
    
    # ===== Mã bên dưới đã bị vô hiệu hóa =====
    if db.is_user_blocked(user_id):
        await update.message.reply_text("Bạn đã bị chặn, không thể sử dụng tính năng này.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Vui lòng dùng /start để đăng ký trước.")
        return

    # Kiểm tra lớp 1: kiểm tra ở cấp bộ xử lý lệnh
    if not db.can_checkin(user_id):
        await update.message.reply_text("❌ Hôm nay bạn đã điểm danh rồi, hãy quay lại vào ngày mai.")
        return

    # Kiểm tra lớp 2: thực thi ở mức cơ sở dữ liệu (giao dịch SQL nguyên tử)
    if db.checkin(user_id):
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"✅ Điểm danh thành công!\nĐiểm nhận được: +1\nĐiểm hiện tại: {user['balance']} điểm"
        )
    else:
        # Nếu lớp cơ sở dữ liệu trả về False, nghĩa là hôm nay đã điểm danh (bảo hiểm kép)
        await update.message.reply_text("❌ Hôm nay bạn đã điểm danh rồi, hãy quay lại vào ngày mai.")


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /invite"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Bạn đã bị chặn, không thể sử dụng tính năng này.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Vui lòng dùng /start để đăng ký trước.")
        return

    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🎁 Liên kết mời riêng của bạn:\n{invite_link}\n\n"
        "Mỗi khi mời thành công 1 người đăng ký, bạn sẽ nhận được 2 điểm."
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /use - dùng mã nạp"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Bạn đã bị chặn, không thể sử dụng tính năng này.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Vui lòng dùng /start để đăng ký trước.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cách dùng: /use <mã_nạp>\n\nVí dụ: /use wandouyu"
        )
        return

    key_code = context.args[0].strip()
    result = db.use_card_key(key_code, user_id)

    if result is None:
        await update.message.reply_text("Mã nạp không tồn tại, vui lòng kiểm tra và thử lại.")
    elif result == -1:
        await update.message.reply_text("Mã nạp này đã đạt giới hạn số lần sử dụng.")
    elif result == -2:
        await update.message.reply_text("Mã nạp này đã hết hạn.")
    elif result == -3:
        await update.message.reply_text("Bạn đã từng dùng mã nạp này rồi.")
    else:
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"Dùng mã nạp thành công!\nĐiểm nhận được: {result}\nĐiểm hiện tại: {user['balance']}"
        )
