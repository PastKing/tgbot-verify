"""Mẫu thông báo"""
from config import CHANNEL_URL, VERIFY_COST, HELP_NOTION_URL


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """Lấy thông báo chào mừng"""
    msg = (
        f"🎉 Chào mừng, {full_name}!\n"
        "Bạn đã đăng ký thành công và nhận được 1 điểm.\n"
    )
    if invited_by:
        msg += "Cảm ơn bạn đã tham gia qua liên kết mời, người mời đã nhận được 2 điểm.\n"

    msg += (
        "\nBot này có thể tự động hoàn tất xác thực SheerID.\n"
        "Bắt đầu nhanh:\n"
        "/about - Xem tính năng bot\n"
        "/balance - Xem số điểm hiện có\n"
        "/help - Xem danh sách lệnh đầy đủ\n\n"
        "Cách nhận thêm điểm:\n"
        "/qd - Điểm danh mỗi ngày\n"
        "/invite - Mời bạn bè\n"
        f"Tham gia kênh: {CHANNEL_URL}"
    )
    return msg


def get_about_message() -> str:
    """Lấy thông báo giới thiệu"""
    return (
        "🤖 Bot tự động xác thực SheerID\n"
        "\n"
        "Giới thiệu tính năng:\n"
        "- Tự động hoàn tất xác thực SheerID cho sinh viên/giáo viên\n"
        "- Hỗ trợ xác thực Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, Bolt.new Teacher\n"
        "\n"
        "Cách nhận điểm:\n"
        "- Đăng ký nhận 1 điểm\n"
        "- Điểm danh hằng ngày +1 điểm\n"
        "- Mời bạn bè +2 điểm/người\n"
        "- Dùng mã nạp điểm theo quy tắc của mã\n"
        f"- Tham gia kênh: {CHANNEL_URL}\n"
        "\n"
        "Cách sử dụng:\n"
        "1. Bắt đầu xác thực trên trang web và sao chép đầy đủ liên kết xác thực\n"
        "2. Gửi /verify, /verify2, /verify3, /verify4 hoặc /verify5 kèm liên kết đó\n"
        "3. Chờ xử lý và xem kết quả\n"
        "4. Xác thực Bolt.new sẽ tự động lấy mã xác thực; nếu cần truy vấn thủ công, dùng /getV4Code <verification_id>\n"
        "\n"
        "Gửi /help để xem thêm lệnh"
    )


def get_help_message(is_admin: bool = False) -> str:
    """Lấy thông báo trợ giúp"""
    msg = (
        "📖 Trợ giúp bot xác thực tự động SheerID\n"
        "\n"
        "Lệnh người dùng:\n"
        "/start - Bắt đầu sử dụng (đăng ký)\n"
        "/about - Xem tính năng bot\n"
        "/balance - Xem số điểm hiện có\n"
        "/qd - Điểm danh hằng ngày (+1 điểm)\n"
        "/invite - Tạo liên kết mời (+2 điểm/người)\n"
        "/use <mã_nạp> - Dùng mã nạp để đổi điểm\n"
        f"/verify <link> - Xác thực Gemini One Pro (-{VERIFY_COST} điểm)\n"
        f"/verify2 <link> - Xác thực ChatGPT Teacher K12 (-{VERIFY_COST} điểm)\n"
        f"/verify3 <link> - Xác thực Spotify Student (-{VERIFY_COST} điểm)\n"
        f"/verify4 <link> - Xác thực Bolt.new Teacher (-{VERIFY_COST} điểm)\n"
        f"/verify5 <link> - Xác thực YouTube Student Premium (-{VERIFY_COST} điểm)\n"
        "/getV4Code <verification_id> - Lấy mã xác thực Bolt.new\n"
        "/help - Xem thông tin trợ giúp này\n"
        f"Hướng dẫn khi xác thực thất bại: {HELP_NOTION_URL}\n"
    )

    if is_admin:
        msg += (
            "\nLệnh quản trị:\n"
            "/addbalance <user_id> <điểm> - Cộng điểm cho người dùng\n"
            "/block <user_id> - Chặn người dùng\n"
            "/white <user_id> - Bỏ chặn người dùng\n"
            "/blacklist - Xem danh sách chặn\n"
            "/genkey <mã_nạp> <điểm> [số_lần] [số_ngày] - Tạo mã nạp\n"
            "/listkeys - Xem danh sách mã nạp\n"
            "/broadcast <văn_bản> - Gửi thông báo hàng loạt cho tất cả người dùng\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """Lấy thông báo không đủ điểm"""
    return (
        f"Không đủ điểm! Cần {VERIFY_COST} điểm, hiện có {current_balance} điểm.\n\n"
        "Cách nhận điểm:\n"
        "- Điểm danh hằng ngày /qd\n"
        "- Mời bạn bè /invite\n"
        "- Dùng mã nạp /use <mã_nạp>"
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """Lấy hướng dẫn dùng lệnh xác thực"""
    return (
        f"Cách dùng: {command} <link SheerID>\n\n"
        "Ví dụ:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "Lấy liên kết xác thực:\n"
        f"1. Mở trang xác thực của {service_name}\n"
        "2. Bắt đầu quy trình xác thực\n"
        "3. Sao chép toàn bộ URL trên thanh địa chỉ trình duyệt\n"
        f"4. Dùng lệnh {command} để gửi"
    )
