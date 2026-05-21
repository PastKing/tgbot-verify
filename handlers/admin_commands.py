"""Bộ xử lý lệnh quản trị"""
import asyncio
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command

logger = logging.getLogger(__name__)


async def addbalance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /addbalance - quản trị cộng điểm"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cách dùng: /addbalance <user_id> <số_điểm>\n\nVí dụ: /addbalance 123456789 10"
        )
        return

    try:
        target_user_id = int(context.args[0])
        amount = int(context.args[1])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("Người dùng không tồn tại.")
            return

        if db.add_balance(target_user_id, amount):
            user = db.get_user(target_user_id)
            await update.message.reply_text(
                f"✅ Đã cộng {amount} điểm cho người dùng {target_user_id}.\n"
                f"Điểm hiện tại: {user['balance']}"
            )
        else:
            await update.message.reply_text("Thao tác thất bại, vui lòng thử lại sau.")
    except ValueError:
        await update.message.reply_text("Định dạng tham số không hợp lệ, vui lòng nhập số hợp lệ.")


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /block - quản trị chặn người dùng"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cách dùng: /block <user_id>\n\nVí dụ: /block 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("Người dùng không tồn tại.")
            return

        if db.block_user(target_user_id):
            await update.message.reply_text(f"✅ Đã chặn người dùng {target_user_id}.")
        else:
            await update.message.reply_text("Thao tác thất bại, vui lòng thử lại sau.")
    except ValueError:
        await update.message.reply_text("Định dạng tham số không hợp lệ, vui lòng nhập user_id hợp lệ.")


async def white_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /white - quản trị bỏ chặn"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cách dùng: /white <user_id>\n\nVí dụ: /white 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("Người dùng không tồn tại.")
            return

        if db.unblock_user(target_user_id):
            await update.message.reply_text(f"✅ Đã bỏ người dùng {target_user_id} khỏi danh sách chặn.")
        else:
            await update.message.reply_text("Thao tác thất bại, vui lòng thử lại sau.")
    except ValueError:
        await update.message.reply_text("Định dạng tham số không hợp lệ, vui lòng nhập user_id hợp lệ.")


async def blacklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /blacklist - xem danh sách chặn"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    blacklist = db.get_blacklist()

    if not blacklist:
        await update.message.reply_text("Danh sách chặn đang trống.")
        return

    msg = "📋 Danh sách chặn:\n\n"
    for user in blacklist:
        msg += f"User ID: {user['user_id']}\n"
        msg += f"Tên người dùng: @{user['username']}\n"
        msg += f"Họ tên: {user['full_name']}\n"
        msg += "---\n"

    await update.message.reply_text(msg)


async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /genkey - quản trị tạo mã nạp"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cách dùng: /genkey <mã_nạp> <điểm> [số_lần_dùng] [số_ngày_hết_hạn]\n\n"
            "Ví dụ:\n"
            "/genkey wandouyu 20 - Tạo mã nạp 20 điểm (dùng một lần, không hết hạn)\n"
            "/genkey vip100 50 10 - Tạo mã nạp 50 điểm (dùng được 10 lần, không hết hạn)\n"
            "/genkey temp 30 1 7 - Tạo mã nạp 30 điểm (dùng một lần, hết hạn sau 7 ngày)"
        )
        return

    try:
        key_code = context.args[0].strip()
        balance = int(context.args[1])
        max_uses = int(context.args[2]) if len(context.args) > 2 else 1
        expire_days = int(context.args[3]) if len(context.args) > 3 else None

        if balance <= 0:
            await update.message.reply_text("Số điểm phải lớn hơn 0.")
            return

        if max_uses <= 0:
            await update.message.reply_text("Số lần sử dụng phải lớn hơn 0.")
            return

        if db.create_card_key(key_code, balance, user_id, max_uses, expire_days):
            msg = (
                "✅ Đã tạo mã nạp thành công!\n\n"
                f"Mã nạp: {key_code}\n"
                f"Điểm: {balance}\n"
                f"Số lần sử dụng: {max_uses} lần\n"
            )
            if expire_days:
                msg += f"Thời hạn: {expire_days} ngày\n"
            else:
                msg += "Thời hạn: vĩnh viễn\n"
            msg += f"\nCách dùng cho người dùng: /use {key_code}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Mã nạp đã tồn tại hoặc tạo thất bại, vui lòng đổi tên mã nạp.")
    except ValueError:
        await update.message.reply_text("Định dạng tham số không hợp lệ, vui lòng nhập số hợp lệ.")


async def listkeys_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /listkeys - quản trị xem danh sách mã nạp"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    keys = db.get_all_card_keys()

    if not keys:
        await update.message.reply_text("Hiện chưa có mã nạp nào.")
        return

    msg = "📋 Danh sách mã nạp:\n\n"
    for key in keys[:20]:  # Chỉ hiển thị 20 mục đầu
        msg += f"Mã nạp: {key['key_code']}\n"
        msg += f"Điểm: {key['balance']}\n"
        msg += f"Số lần sử dụng: {key['current_uses']}/{key['max_uses']}\n"

        if key["expire_at"]:
            expire_time = datetime.fromisoformat(key["expire_at"])
            if datetime.now() > expire_time:
                msg += "Trạng thái: đã hết hạn\n"
            else:
                days_left = (expire_time - datetime.now()).days
                msg += f"Trạng thái: còn hiệu lực (còn {days_left} ngày)\n"
        else:
            msg += "Trạng thái: hiệu lực vĩnh viễn\n"

        msg += "---\n"

    if len(keys) > 20:
        msg += f"\n(Chỉ hiển thị 20 mục đầu, tổng cộng {len(keys)} mục)"

    await update.message.reply_text(msg)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Xử lý lệnh /broadcast - quản trị gửi thông báo hàng loạt"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    text = " ".join(context.args).strip() if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or ""

    if not text:
        await update.message.reply_text("Cách dùng: /broadcast <văn_bản>, hoặc trả lời một tin nhắn rồi gửi /broadcast")
        return

    user_ids = db.get_all_user_ids()
    success, failed = 0, 0

    status_msg = await update.message.reply_text(f"📢 Bắt đầu gửi hàng loạt, tổng cộng {len(user_ids)} người dùng...")

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
            success += 1
                await asyncio.sleep(0.05)  # Hạn chế tốc độ để tránh bị giới hạn
        except Exception as e:
                logger.warning("Gửi đến %s thất bại: %s", uid, e)
            failed += 1

            await status_msg.edit_text(f"✅ Gửi hàng loạt hoàn tất!\nThành công: {success}\nThất bại: {failed}")
