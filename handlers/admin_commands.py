"""Admin command handlers"""
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
    """Handle /addbalance command - admin add points"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /addbalance <user_id> <points>\n\nExample: /addbalance 123456789 10"
        )
        return

    try:
        target_user_id = int(context.args[0])
        amount = int(context.args[1])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("User not found.")
            return

        if db.add_balance(target_user_id, amount):
            user = db.get_user(target_user_id)
            await update.message.reply_text(
                f"✅ Added {amount} points to user {target_user_id}.\n"
                f"Current points: {user['balance']}"
            )
        else:
            await update.message.reply_text("Operation failed. Please try again later.")
    except ValueError:
        await update.message.reply_text("Invalid format. Please enter valid numbers.")


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /block command - admin block user"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /block <user_id>\n\nExample: /block 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("User not found.")
            return

        if db.block_user(target_user_id):
            await update.message.reply_text(f"✅ User {target_user_id} has been blocked.")
        else:
            await update.message.reply_text("Operation failed. Please try again later.")
    except ValueError:
        await update.message.reply_text("Invalid format. Please enter a valid user ID.")


async def white_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /white command - admin unblock user"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /white <user_id>\n\nExample: /white 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("User not found.")
            return

        if db.unblock_user(target_user_id):
            await update.message.reply_text(f"✅ User {target_user_id} has been removed from the blacklist.")
        else:
            await update.message.reply_text("Operation failed. Please try again later.")
    except ValueError:
        await update.message.reply_text("Invalid format. Please enter a valid user ID.")


async def blacklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /blacklist command - view blacklist"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    blacklist = db.get_blacklist()

    if not blacklist:
        await update.message.reply_text("Blacklist is empty.")
        return

    msg = "📋 Blacklist:\n\n"
    for user in blacklist:
        msg += f"User ID: {user['user_id']}\n"
        msg += f"Username: @{user['username']}\n"
        msg += f"Name: {user['full_name']}\n"
        msg += "---\n"

    await update.message.reply_text(msg)


async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /genkey command - admin generate redemption code"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /genkey <code> <points> [uses] [days]\n\n"
            "Examples:\n"
            "/genkey wandouyu 20 - 20 points (single-use, never expires)\n"
            "/genkey vip100 50 10 - 50 points (10 uses, never expires)\n"
            "/genkey temp 30 1 7 - 30 points (single-use, expires in 7 days)"
        )
        return

    try:
        key_code = context.args[0].strip()
        balance = int(context.args[1])
        max_uses = int(context.args[2]) if len(context.args) > 2 else 1
        expire_days = int(context.args[3]) if len(context.args) > 3 else None

        if balance <= 0:
            await update.message.reply_text("Points must be greater than 0.")
            return

        if max_uses <= 0:
            await update.message.reply_text("Uses must be greater than 0.")
            return

        if db.create_card_key(key_code, balance, user_id, max_uses, expire_days):
            msg = (
                "✅ Redemption code created successfully!\n\n"
                f"Code: {key_code}\n"
                f"Points: {balance}\n"
                f"Max uses: {max_uses}\n"
            )
            if expire_days:
                msg += f"Validity: {expire_days} days\n"
            else:
                msg += "Validity: never expires\n"
            msg += f"\nUser usage: /use {key_code}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Code already exists or creation failed. Please use another code.")
    except ValueError:
        await update.message.reply_text("Invalid format. Please enter valid numbers.")


async def listkeys_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /listkeys command - admin view code list"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    keys = db.get_all_card_keys()

    if not keys:
        await update.message.reply_text("No redemption codes available.")
        return

    msg = "📋 Redemption Codes:\n\n"
    for key in keys[:20]:  # show top 20
        msg += f"Code: {key['key_code']}\n"
        msg += f"Points: {key['balance']}\n"
        msg += f"Uses: {key['current_uses']}/{key['max_uses']}\n"

        if key["expire_at"]:
            expire_time = datetime.fromisoformat(key["expire_at"])
            if datetime.now() > expire_time:
                msg += "Status: expired\n"
            else:
                days_left = (expire_time - datetime.now()).days
                msg += f"Status: active ({days_left} days left)\n"
        else:
            msg += "Status: never expires\n"

        msg += "---\n"

    if len(keys) > 20:
        msg += f"\n(Showing first 20 of {len(keys)})"

    await update.message.reply_text(msg)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /broadcast command - admin broadcast notification"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    text = " ".join(context.args).strip() if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or ""

    if not text:
        await update.message.reply_text(
            "Usage: /broadcast <text>, or reply to a message and send /broadcast"
        )
        return

    user_ids = db.get_all_user_ids()
    success, failed = 0, 0

    status_msg = await update.message.reply_text(
        f"📢 Starting broadcast to {len(user_ids)} users..."
    )

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
            success += 1
            await asyncio.sleep(0.05)  # rate limit to avoid restrictions
        except Exception as e:
            logger.warning("Broadcast to %s failed: %s", uid, e)
            failed += 1

    await status_msg.edit_text(
        f"✅ Broadcast complete!\nSuccess: {success}\nFailed: {failed}"
    )
