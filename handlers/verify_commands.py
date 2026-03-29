"""验证命令处理器"""
import asyncio
import logging
import httpx
import time
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import VERIFY_COST
from database_mysql import Database
from one.sheerid_verifier import SheerIDVerifier as OneVerifier
from k12.sheerid_verifier import SheerIDVerifier as K12Verifier
from spotify.sheerid_verifier import SheerIDVerifier as SpotifyVerifier
from youtube.sheerid_verifier import SheerIDVerifier as YouTubeVerifier
from Boltnew.sheerid_verifier import SheerIDVerifier as BoltnewVerifier
from utils.messages import get_insufficient_balance_message, get_verify_usage_message

# 尝试导入并发控制，如果失败则使用空实现
try:
    from utils.concurrency import get_verification_semaphore
except ImportError:
    # 如果导入失败，创建一个简单的实现
    def get_verification_semaphore(verification_type: str):
        return asyncio.Semaphore(3)

logger = logging.getLogger(__name__)


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify 命令 - Gemini One Pro"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("您已被拉黑，无法使用此功能。")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("请先使用 /start 注册。")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify", "Gemini One Pro")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    verification_id = OneVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("无效的 SheerID 链接，请检查后重试。")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("扣除积分失败，请稍后重试。")
        return

    processing_msg = await update.message.reply_text(
        f"开始处理 Gemini One Pro 认证...\n"
        f"验证ID: {verification_id}\n"
        f"已扣除 {VERIFY_COST} 积分\n\n"
        "请稍候，这可能需要 1-2 分钟..."
    )

    try:
        verifier = OneVerifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "gemini_one_pro",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ 认证成功！\n\n"
            if result.get("pending"):
                result_msg += "文档已提交，等待人工审核。\n"
            if result.get("redirect_url"):
                result_msg += f"跳转链接：\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ 认证失败：{result.get('message', '未知错误')}\n\n"
                f"已退回 {VERIFY_COST} 积分"
            )
    except Exception as e:
        logger.error("验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ 处理过程中出现错误：{str(e)}\n\n"
            f"已退回 {VERIFY_COST} 积分"
        )


async def verify2_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify2 命令 - ChatGPT Teacher K12"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("您已被拉黑，无法使用此功能。")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("请先使用 /start 注册。")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify2", "ChatGPT Teacher K12")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    verification_id = K12Verifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("无效的 SheerID 链接，请检查后重试。")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("扣除积分失败，请稍后重试。")
        return

    processing_msg = await update.message.reply_text(
        f"开始处理 ChatGPT Teacher K12 认证...\n"
        f"验证ID: {verification_id}\n"
        f"已扣除 {VERIFY_COST} 积分\n\n"
        "请稍候，这可能需要 1-2 分钟..."
    )

    try:
        verifier = K12Verifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "chatgpt_teacher_k12",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ 认证成功！\n\n"
            if result.get("pending"):
                result_msg += "文档已提交，等待人工审核。\n"
            if result.get("redirect_url"):
                result_msg += f"跳转链接：\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ 认证失败：{result.get('message', '未知错误')}\n\n"
                f"已退回 {VERIFY_COST} 积分"
            )
    except Exception as e:
        logger.error("验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ 处理过程中出现错误：{str(e)}\n\n"
            f"已退回 {VERIFY_COST} 积分"
        )


async def verify3_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify3 命令 - Spotify Student"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("您已被拉黑，无法使用此功能。")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("请先使用 /start 注册。")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify3", "Spotify Student")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    # 解析 verificationId
    verification_id = SpotifyVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("无效的 SheerID 链接，请检查后重试。")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("扣除积分失败，请稍后重试。")
        return

    processing_msg = await update.message.reply_text(
        f"🎵 开始处理 Spotify Student 认证...\n"
        f"已扣除 {VERIFY_COST} 积分\n\n"
        "📝 正在生成学生信息...\n"
        "🎨 正在生成学生证 PNG...\n"
        "📤 正在提交文档..."
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("spotify_student")

    try:
        async with semaphore:
            verifier = SpotifyVerifier(verification_id)
            result = await asyncio.to_thread(verifier.verify)

            db.add_verification(
                user_id,
                "spotify_student",
                url,
                "success" if result["success"] else "failed",
                str(result),
            )

            if result["success"]:
                result_msg = "✅ Spotify 学生认证成功！\n\n"
                if result.get("pending"):
                    result_msg += "✨ 文档已提交，等待 SheerID 审核\n"
                    result_msg += "⏱️ 预计审核时间：几分钟内\n\n"
                if result.get("redirect_url"):
                    result_msg += f"🔗 跳转链接：\n{result['redirect_url']}"
                await processing_msg.edit_text(result_msg)
            else:
                db.add_balance(user_id, VERIFY_COST)
                await processing_msg.edit_text(
                    f"❌ 认证失败：{result.get('message', '未知错误')}\n\n"
                    f"已退回 {VERIFY_COST} 积分"
                )
    except Exception as e:
        logger.error("Spotify 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ 处理过程中出现错误：{str(e)}\n\n"
            f"已退回 {VERIFY_COST} 积分"
        )


async def verify4_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify4 命令 - Bolt.new Teacher（自动获取code版）"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("您已被拉黑，无法使用此功能。")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("请先使用 /start 注册。")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify4", "Bolt.new Teacher")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    # 解析 externalUserId 或 verificationId
    external_user_id = BoltnewVerifier.parse_external_user_id(url)
    verification_id = BoltnewVerifier.parse_verification_id(url)

    if not external_user_id and not verification_id:
        await update.message.reply_text("无效的 SheerID 链接，请检查后重试。")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("扣除积分失败，请稍后重试。")
        return

    processing_msg = await update.message.reply_text(
        f"🚀 开始处理 Bolt.new Teacher 认证...\n"
        f"已扣除 {VERIFY_COST} 积分\n\n"
        "📤 正在提交文档..."
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("bolt_teacher")

    try:
        async with semaphore:
            # 第1步：提交文档
            verifier = BoltnewVerifier(url, verification_id=verification_id)
            result = await asyncio.to_thread(verifier.verify)

        if not result.get("success"):
            # 提交失败，退款
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ 文档提交失败：{result.get('message', '未知错误')}\n\n"
                f"已退回 {VERIFY_COST} 积分"
            )
            return
        
        vid = result.get("verification_id", "")
        if not vid:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ 未获取到验证ID\n\n"
                f"已退回 {VERIFY_COST} 积分"
            )
            return
        
        # 更新消息
        await processing_msg.edit_text(
            f"✅ 文档已提交！\n"
            f"📋 验证ID: `{vid}`\n\n"
            f"🔍 正在自动获取认证码...\n"
            f"（最多等待20秒）"
        )
        
        # 第2步：自动获取认证码（最多20秒）
        code = await _auto_get_reward_code(vid, max_wait=20, interval=5)
        
        if code:
            # 成功获取
            result_msg = (
                f"🎉 认证成功！\n\n"
                f"✅ 文档已提交\n"
                f"✅ 审核已通过\n"
                f"✅ 认证码已获取\n\n"
                f"🎁 认证码: `{code}`\n"
            )
            if result.get("redirect_url"):
                result_msg += f"\n🔗 跳转链接:\n{result['redirect_url']}"
            
            await processing_msg.edit_text(result_msg)
            
            # 保存成功记录
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "success",
                f"Code: {code}",
                vid
            )
        else:
            # 20秒内未获取到，让用户稍后查询
            await processing_msg.edit_text(
                f"✅ 文档已提交成功！\n\n"
                f"⏳ 认证码尚未生成（可能需要1-5分钟审核）\n\n"
                f"📋 验证ID: `{vid}`\n\n"
                f"💡 请稍后使用以下命令查询:\n"
                f"`/getV4Code {vid}`\n\n"
                f"注意：积分已消耗，稍后查询无需再付费"
            )
            
            # 保存待处理记录
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "pending",
                "Waiting for review",
                vid
            )
            
    except Exception as e:
        logger.error("Bolt.new 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ 处理过程中出现错误：{str(e)}\n\n"
            f"已退回 {VERIFY_COST} 积分"
        )


async def _auto_get_reward_code(
    verification_id: str,
    max_wait: int = 20,
    interval: int = 5
) -> Optional[str]:
    """自动获取认证码（轻量级轮询，不影响并发）
    
    Args:
        verification_id: 验证ID
        max_wait: 最大等待时间（秒）
        interval: 轮询间隔（秒）
        
    Returns:
        str: 认证码，如果获取失败返回None
    """
    import time
    start_time = time.time()
    attempts = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            elapsed = int(time.time() - start_time)
            attempts += 1
            
            # 检查是否超时
            if elapsed >= max_wait:
                logger.info(f"自动获取code超时({elapsed}秒)，让用户手动查询")
                return None
            
            try:
                # 查询验证状态
                response = await client.get(
                    f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    current_step = data.get("currentStep")
                    
                    if current_step == "success":
                        # 获取认证码
                        code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
                        if code:
                            logger.info(f"✅ 自动获取code成功: {code} (耗时{elapsed}秒)")
                            return code
                    elif current_step == "error":
                        # 审核失败
                        logger.warning(f"审核失败: {data.get('errorIds', [])}")
                        return None
                    # else: pending，继续等待
                
                # 等待下次轮询
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.warning(f"查询认证码出错: {e}")
                await asyncio.sleep(interval)
    
    return None


async def verify5_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify5 命令 - YouTube Student Premium"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("您已被拉黑，无法使用此功能。")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("请先使用 /start 注册。")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify5", "YouTube Student Premium")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    # 解析 verificationId
    verification_id = YouTubeVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("无效的 SheerID 链接，请检查后重试。")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("扣除积分失败，请稍后重试。")
        return

    processing_msg = await update.message.reply_text(
        f"📺 开始处理 YouTube Student Premium 认证...\n"
        f"已扣除 {VERIFY_COST} 积分\n\n"
        "📝 正在生成学生信息...\n"
        "🎨 正在生成学生证 PNG...\n"
        "📤 正在提交文档..."
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("youtube_student")

    try:
        async with semaphore:
            verifier = YouTubeVerifier(verification_id)
            result = await asyncio.to_thread(verifier.verify)

            db.add_verification(
                user_id,
                "youtube_student",
                url,
                "success" if result["success"] else "failed",
                str(result),
            )

            if result["success"]:
                result_msg = "✅ YouTube Student Premium 认证成功！\n\n"
                if result.get("pending"):
                    result_msg += "✨ 文档已提交，等待 SheerID 审核\n"
                    result_msg += "⏱️ 预计审核时间：几分钟内\n\n"
                if result.get("redirect_url"):
                    result_msg += f"🔗 跳转链接：\n{result['redirect_url']}"
                await processing_msg.edit_text(result_msg)
            else:
                db.add_balance(user_id, VERIFY_COST)
                await processing_msg.edit_text(
                    f"❌ 认证失败：{result.get('message', '未知错误')}\n\n"
                    f"已退回 {VERIFY_COST} 积分"
                )
    except Exception as e:
        logger.error("YouTube 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ 处理过程中出现错误：{str(e)}\n\n"
            f"已退回 {VERIFY_COST} 积分"
        )


async def getV4Code_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /getV4Code 命令 - 获取 Bolt.new Teacher 认证码"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("您已被拉黑，无法使用此功能。")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("请先使用 /start 注册。")
        return

    # 检查是否提供了 verification_id
    if not context.args:
        await update.message.reply_text(
            "使用方法: /getV4Code <verification_id>\n\n"
            "示例: /getV4Code 6929436b50d7dc18638890d0\n\n"
            "verification_id 在使用 /verify4 命令后会返回给您。"
        )
        return

    verification_id = context.args[0].strip()

    processing_msg = await update.message.reply_text(
        "🔍 正在查询认证码，请稍候..."
    )

    try:
        # 查询 SheerID API 获取认证码
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
            )

            if response.status_code != 200:
                await processing_msg.edit_text(
                    f"❌ 查询失败，状态码：{response.status_code}\n\n"
                    "请稍后重试或联系管理员。"
                )
                return

            data = response.json()
            current_step = data.get("currentStep")
            reward_code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
            redirect_url = data.get("redirectUrl")

            if current_step == "success" and reward_code:
                result_msg = "✅ 认证成功！\n\n"
                result_msg += f"🎉 认证码：`{reward_code}`\n\n"
                if redirect_url:
                    result_msg += f"跳转链接：\n{redirect_url}"
                await processing_msg.edit_text(result_msg)
            elif current_step == "pending":
                await processing_msg.edit_text(
                    "⏳ 认证仍在审核中，请稍后再试。\n\n"
                    "通常需要 1-5 分钟，请耐心等待。"
                )
            elif current_step == "error":
                error_ids = data.get("errorIds", [])
                await processing_msg.edit_text(
                    f"❌ 认证失败\n\n"
                    f"错误信息：{', '.join(error_ids) if error_ids else '未知错误'}"
                )
            else:
                await processing_msg.edit_text(
                    f"⚠️ 当前状态：{current_step}\n\n"
                    "认证码尚未生成，请稍后重试。"
                )

    except Exception as e:
        logger.error("获取 Bolt.new 认证码失败: %s", e)
        await processing_msg.edit_text(
            f"❌ 查询过程中出现错误：{str(e)}\n\n"
            "请稍后重试或联系管理员。"
      )
