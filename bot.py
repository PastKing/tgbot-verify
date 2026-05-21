"""Chương trình chính của bot Telegram"""
import logging
from functools import partial

from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from database_mysql import Database
from handlers.user_commands import (
    start_command,
    about_command,
    help_command,
    balance_command,
    checkin_command,
    invite_command,
    use_command,
)
from handlers.verify_commands import (
    verify_command,
    verify2_command,
    verify3_command,
    verify4_command,
    getV4Code_command,
)
from handlers.admin_commands import (
    addbalance_command,
    block_command,
    white_command,
    blacklist_command,
    genkey_command,
    listkeys_command,
    broadcast_command,
)

# Cấu hình log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context) -> None:
    """Xử lý lỗi toàn cục"""
    logger.exception("Đã xảy ra ngoại lệ khi xử lý cập nhật: %s", context.error, exc_info=context.error)


def main():
    """Hàm chính"""
    # Khởi tạo cơ sở dữ liệu
    db = Database()

    # Tạo ứng dụng - bật xử lý đồng thời
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)  # 🔥 Quan trọng: bật xử lý đồng thời nhiều lệnh
        .build()
    )

    # Đăng ký lệnh người dùng (dùng partial để truyền tham số db)
    application.add_handler(CommandHandler("start", partial(start_command, db=db)))
    application.add_handler(CommandHandler("about", partial(about_command, db=db)))
    application.add_handler(CommandHandler("help", partial(help_command, db=db)))
    application.add_handler(CommandHandler("balance", partial(balance_command, db=db)))
    application.add_handler(CommandHandler("qd", partial(checkin_command, db=db)))
    application.add_handler(CommandHandler("invite", partial(invite_command, db=db)))
    application.add_handler(CommandHandler("use", partial(use_command, db=db)))

    # Đăng ký lệnh xác thực
    application.add_handler(CommandHandler("verify", partial(verify_command, db=db)))
    application.add_handler(CommandHandler("verify2", partial(verify2_command, db=db)))
    application.add_handler(CommandHandler("verify3", partial(verify3_command, db=db)))
    application.add_handler(CommandHandler("verify4", partial(verify4_command, db=db)))
    application.add_handler(CommandHandler("getV4Code", partial(getV4Code_command, db=db)))

    # Đăng ký lệnh quản trị
    application.add_handler(CommandHandler("addbalance", partial(addbalance_command, db=db)))
    application.add_handler(CommandHandler("block", partial(block_command, db=db)))
    application.add_handler(CommandHandler("white", partial(white_command, db=db)))
    application.add_handler(CommandHandler("blacklist", partial(blacklist_command, db=db)))
    application.add_handler(CommandHandler("genkey", partial(genkey_command, db=db)))
    application.add_handler(CommandHandler("listkeys", partial(listkeys_command, db=db)))
    application.add_handler(CommandHandler("broadcast", partial(broadcast_command, db=db)))

    # Đăng ký bộ xử lý lỗi
    application.add_error_handler(error_handler)

    logger.info("Bot đang khởi động...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
