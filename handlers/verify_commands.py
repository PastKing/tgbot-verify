"""Verification command handlers"""
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

# Try to import concurrency control, fallback to a simple implementation
try:
    from utils.concurrency import get_verification_semaphore
except ImportError:
    # If import fails, create a simple implementation
    def get_verification_semaphore(verification_type: str):
        return asyncio.Semaphore(3)

logger = logging.getLogger(__name__)


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /verify command - Gemini One Pro"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You are blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
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
        await update.message.reply_text("Invalid SheerID link. Please check and try again.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Failed to deduct points. Please try again later.")
        return

    processing_msg = await update.message.reply_text(
        f"Starting Gemini One Pro verification...\n"
        f"Verification ID: {verification_id}\n"
        f"Deducted {VERIFY_COST} points\n\n"
        "Please wait. This may take 1-2 minutes..."
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
            result_msg = "✅ Verification succeeded!\n\n"
            if result.get("pending"):
                result_msg += "Documents submitted. Awaiting manual review.\n"
            if result.get("redirect_url"):
                result_msg += f"Redirect link:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verification failed: {result.get('message', 'Unknown error')}\n\n"
                f"Refunded {VERIFY_COST} points"
            )
    except Exception as e:
        logger.error("Verification error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Error during processing: {str(e)}\n\n"
            f"Refunded {VERIFY_COST} points"
        )


async def verify2_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /verify2 command - ChatGPT Teacher K12"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You are blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
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
        await update.message.reply_text("Invalid SheerID link. Please check and try again.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Failed to deduct points. Please try again later.")
        return

    processing_msg = await update.message.reply_text(
        f"Starting ChatGPT Teacher K12 verification...\n"
        f"Verification ID: {verification_id}\n"
        f"Deducted {VERIFY_COST} points\n\n"
        "Please wait. This may take 1-2 minutes..."
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
            result_msg = "✅ Verification succeeded!\n\n"
            if result.get("pending"):
                result_msg += "Documents submitted. Awaiting manual review.\n"
            if result.get("redirect_url"):
                result_msg += f"Redirect link:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verification failed: {result.get('message', 'Unknown error')}\n\n"
                f"Refunded {VERIFY_COST} points"
            )
    except Exception as e:
        logger.error("Verification error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Error during processing: {str(e)}\n\n"
            f"Refunded {VERIFY_COST} points"
        )


async def verify3_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /verify3 command - Spotify Student"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You are blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
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

    # Parse verificationId
    verification_id = SpotifyVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Invalid SheerID link. Please check and try again.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Failed to deduct points. Please try again later.")
        return

    processing_msg = await update.message.reply_text(
        f"🎵 Starting Spotify Student verification...\n"
        f"Deducted {VERIFY_COST} points\n\n"
        "📝 Generating student info...\n"
        "🎨 Generating student ID PNG...\n"
        "📤 Submitting documents..."
    )

    # Use semaphore to control concurrency
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
            result_msg = "✅ Spotify Student verification succeeded!\n\n"
            if result.get("pending"):
                result_msg += "✨ Documents submitted. Awaiting SheerID review\n"
                result_msg += "⏱️ Estimated review time: a few minutes\n\n"
            if result.get("redirect_url"):
                result_msg += f"🔗 Redirect link:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verification failed: {result.get('message', 'Unknown error')}\n\n"
                f"Refunded {VERIFY_COST} points"
            )
    except Exception as e:
        logger.error("Spotify verification error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Error during processing: {str(e)}\n\n"
            f"Refunded {VERIFY_COST} points"
        )


async def verify4_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /verify4 command - Bolt.new Teacher (auto code)"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You are blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
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

    # Parse externalUserId or verificationId
    external_user_id = BoltnewVerifier.parse_external_user_id(url)
    verification_id = BoltnewVerifier.parse_verification_id(url)

    if not external_user_id and not verification_id:
        await update.message.reply_text("Invalid SheerID link. Please check and try again.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Failed to deduct points. Please try again later.")
        return

    processing_msg = await update.message.reply_text(
        f"🚀 Starting Bolt.new Teacher verification...\n"
        f"Deducted {VERIFY_COST} points\n\n"
        "📤 Submitting documents..."
    )

    # Use semaphore to control concurrency
    semaphore = get_verification_semaphore("bolt_teacher")

    try:
        async with semaphore:
            # Step 1: submit documents
            verifier = BoltnewVerifier(url, verification_id=verification_id)
            result = await asyncio.to_thread(verifier.verify)

        if not result.get("success"):
            # Submit failed, refund
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Document submission failed: {result.get('message', 'Unknown error')}\n\n"
                f"Refunded {VERIFY_COST} points"
            )
            return

        vid = result.get("verification_id", "")
        if not vid:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Failed to obtain verification ID\n\n"
                f"Refunded {VERIFY_COST} points"
            )
            return

        # Update message
        await processing_msg.edit_text(
            f"✅ Documents submitted!\n"
            f"📋 Verification ID: `{vid}`\n\n"
            f"🔍 Automatically fetching verification code...\n"
            f"(up to 20 seconds)"
        )

        # Step 2: auto get code (up to 20 seconds)
        code = await _auto_get_reward_code(vid, max_wait=20, interval=5)

        if code:
            # Success
            result_msg = (
                f"🎉 Verification succeeded!\n\n"
                f"✅ Documents submitted\n"
                f"✅ Review passed\n"
                f"✅ Verification code obtained\n\n"
                f"🎁 Code: `{code}`\n"
            )
            if result.get("redirect_url"):
                result_msg += f"\n🔗 Redirect link:\n{result['redirect_url']}"

            await processing_msg.edit_text(result_msg)

            # Save success record
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "success",
                f"Code: {code}",
                vid,
            )
        else:
            # Not obtained within 20 seconds, let user query later
            await processing_msg.edit_text(
                f"✅ Documents submitted successfully!\n\n"
                f"⏳ Verification code not generated yet (review may take 1-5 minutes)\n\n"
                f"📋 Verification ID: `{vid}`\n\n"
                f"💡 Please use the following command later:\n"
                f"`/getV4Code {vid}`\n\n"
                f"Note: points have been consumed; later query is free."
            )

            # Save pending record
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "pending",
                "Waiting for review",
                vid,
            )

    except Exception as e:
        logger.error("Bolt.new verification error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Error during processing: {str(e)}\n\n"
            f"Refunded {VERIFY_COST} points"
        )


async def _auto_get_reward_code(
    verification_id: str,
    max_wait: int = 20,
    interval: int = 5
) -> Optional[str]:
    """Auto fetch verification code (light polling, no concurrency impact)

    Args:
        verification_id: Verification ID
        max_wait: Max wait time (seconds)
        interval: Polling interval (seconds)

    Returns:
        str: Code, or None if not available
    """
    import time
    start_time = time.time()
    attempts = 0

    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            elapsed = int(time.time() - start_time)
            attempts += 1

            # Timeout check
            if elapsed >= max_wait:
                logger.info(f"Auto code fetch timed out ({elapsed}s), asking user to query manually")
                return None

            try:
                # Query verification status
                response = await client.get(
                    f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
                )

                if response.status_code == 200:
                    data = response.json()
                    current_step = data.get("currentStep")

                    if current_step == "success":
                        # Get code
                        code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
                        if code:
                            logger.info(f"✅ Auto code fetch succeeded: {code} ({elapsed}s)")
                            return code
                    elif current_step == "error":
                        # Review failed
                        logger.warning(f"Review failed: {data.get('errorIds', [])}")
                        return None
                    # else: pending, continue

                # Wait for next polling
                await asyncio.sleep(interval)

            except Exception as e:
                logger.warning(f"Error while fetching code: {e}")
                await asyncio.sleep(interval)

    return None


async def verify5_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /verify5 command - YouTube Student Premium"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You are blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
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

    # Parse verificationId
    verification_id = YouTubeVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Invalid SheerID link. Please check and try again.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Failed to deduct points. Please try again later.")
        return

    processing_msg = await update.message.reply_text(
        f"📺 Starting YouTube Student Premium verification...\n"
        f"Deducted {VERIFY_COST} points\n\n"
        "📝 Generating student info...\n"
        "🎨 Generating student ID PNG...\n"
        "📤 Submitting documents..."
    )

    # Use semaphore to control concurrency
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
            result_msg = "✅ YouTube Student Premium verification succeeded!\n\n"
            if result.get("pending"):
                result_msg += "✨ Documents submitted. Awaiting SheerID review\n"
                result_msg += "⏱️ Estimated review time: a few minutes\n\n"
            if result.get("redirect_url"):
                result_msg += f"🔗 Redirect link:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verification failed: {result.get('message', 'Unknown error')}\n\n"
                f"Refunded {VERIFY_COST} points"
            )
    except Exception as e:
        logger.error("YouTube verification error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Error during processing: {str(e)}\n\n"
            f"Refunded {VERIFY_COST} points"
        )


async def getV4Code_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /getV4Code command - get Bolt.new Teacher verification code"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("You are blocked and cannot use this feature.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Please register first using /start.")
        return

    # Check if verification_id provided
    if not context.args:
        await update.message.reply_text(
            "Usage: /getV4Code <verification_id>\n\n"
            "Example: /getV4Code 6929436b50d7dc18638890d0\n\n"
            "The verification_id is returned after /verify4."
        )
        return

    verification_id = context.args[0].strip()

    processing_msg = await update.message.reply_text(
        "🔍 Querying verification code, please wait..."
    )

    try:
        # Query SheerID API for code
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
            )

            if response.status_code != 200:
                await processing_msg.edit_text(
                    f"❌ Query failed. Status code: {response.status_code}\n\n"
                    "Please try again later or contact admin."
                )
                return

            data = response.json()
            current_step = data.get("currentStep")
            reward_code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
            redirect_url = data.get("redirectUrl")

            if current_step == "success" and reward_code:
                result_msg = "✅ Verification succeeded!\n\n"
                result_msg += f"🎉 Code: `{reward_code}`\n\n"
                if redirect_url:
                    result_msg += f"Redirect link:\n{redirect_url}"
                await processing_msg.edit_text(result_msg)
            elif current_step == "pending":
                await processing_msg.edit_text(
                    "⏳ Verification is still under review. Please try again later.\n\n"
                    "Usually takes 1-5 minutes."
                )
            elif current_step == "error":
                error_ids = data.get("errorIds", [])
                await processing_msg.edit_text(
                    "❌ Verification failed\n\n"
                    f"Error: {', '.join(error_ids) if error_ids else 'Unknown error'}"
                )
            else:
                await processing_msg.edit_text(
                    f"⚠️ Current status: {current_step}\n\n"
                    "Verification code not generated yet. Please try again later."
                )

    except Exception as e:
        logger.error("Failed to get Bolt.new code: %s", e)
        await processing_msg.edit_text(
            f"❌ Error during query: {str(e)}\n\n"
            "Please try again later or contact admin."
        )
