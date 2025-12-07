"""消息模板"""
from config import CHANNEL_URL, VERIFY_COST, HELP_NOTION_URL


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """获取欢迎消息"""
    msg = (
        f"🎉 欢迎，{full_name}！\n"
        "您已成功注册，获得 1 积分。\n"
    )
    if invited_by:
        msg += "感谢通过邀请链接加入，邀请人已获得 2 积分。\n"

    msg += (
        "\n本机器人可自动完成 SheerID 认证。\n"
        "快速开始：\n"
        "/about - 了解机器人功能\n"
        "/balance - 查看积分余额\n"
        "/help - 查看完整命令列表\n\n"
        "获取更多积分：\n"
        "/qd - 每日签到\n"
        "/invite - 邀请好友\n"
        f"加入频道：{CHANNEL_URL}"
    )
    return msg


def get_about_message() -> str:
    """获取关于消息"""
    return (
        "🤖 SheerID 自动认证机器人\n"
        "\n"
        "功能介绍:\n"
        "- 自动完成 SheerID 学生/教师认证\n"
        "- 支持 Gemini One Pro、ChatGPT Teacher K12、Bolt.new Teacher 认证\n"
        "\n"
        "积分获取:\n"
        "- 注册赠送 1 积分\n"
        "- 每日签到 +1 积分\n"
        "- 邀请好友 +2 积分/人\n"
        "- 使用卡密（按卡密规则）\n"
        f"- 加入频道：{CHANNEL_URL}\n"
        "\n"
        "使用方法:\n"
        "1. 在网页开始认证并复制完整的验证链接\n"
        "2. 发送 /verify、/verify2 或 /verify4 携带该链接\n"
        "3. 等待处理并查看结果\n"
        "4. Bolt.new 认证会自动获取认证码，如需手动查询使用 /getV4Code <verification_id>\n"
        "\n"
        "更多命令请发送 /help"
    )


def get_help_message(is_admin: bool = False) -> str:
    """获取帮助消息"""
    msg = (
        "📖 SheerID 自动认证机器人 - 帮助\n"
        "\n"
        "用户命令:\n"
        "/start - 开始使用（注册）\n"
        "/about - 了解机器人功能\n"
        "/balance - 查看积分余额\n"
        "/qd - 每日签到（+1积分）\n"
        "/invite - 生成邀请链接（+2积分/人）\n"
        "/use <卡密> - 使用卡密兑换积分\n"
        f"/verify <链接> - Gemini One Pro 认证（-{VERIFY_COST}积分）\n"
        f"/verify2 <链接> - ChatGPT Teacher K12 认证（-{VERIFY_COST}积分）\n"
        f"/verify4 <链接> - Bolt.new Teacher 认证（-{VERIFY_COST}积分）\n"
        "/getV4Code <verification_id> - 获取 Bolt.new 认证码\n"
        "/help - 查看此帮助信息\n"
        f"认证失败查看：{HELP_NOTION_URL}\n"
    )

    if is_admin:
        msg += (
            "\n管理员命令:\n"
            "/addbalance <用户ID> <积分> - 增加用户积分\n"
            "/block <用户ID> - 拉黑用户\n"
            "/white <用户ID> - 取消拉黑\n"
            "/blacklist - 查看黑名单\n"
            "/genkey <卡密> <积分> [次数] [天数] - 生成卡密\n"
            "/listkeys - 查看卡密列表\n"
            "/broadcast <文本> - 向所有用户群发通知\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """获取积分不足消息"""
    return (
        f"积分不足！需要 {VERIFY_COST} 积分，当前 {current_balance} 积分。\n\n"
        "获取积分方式:\n"
        "- 每日签到 /qd\n"
        "- 邀请好友 /invite\n"
        "- 使用卡密 /use <卡密>"
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """获取验证命令使用说明"""
    return (
        f"使用方法: {command} <SheerID链接>\n\n"
        "示例:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "获取验证链接:\n"
        f"1. 访问 {service_name} 认证页面\n"
        "2. 开始认证流程\n"
        "3. 复制浏览器地址栏中的完整 URL\n"
        f"4. 使用 {command} 命令提交"
    )
