import logging
import asyncio
from config import REQUIRED_CHANNELS
from database import get_file_id
from utils import is_user_in_channels
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest

# Start command handler (Deep Link for File Download)
async def start(update, context):
    user_id = update.message.from_user.id
    app = context.application

    # Log the start command and arguments
    logging.info(f"User {user_id} triggered /start with args: {context.args}")

    # Get short ID from deep link
    args = context.args
    if args:
        short_id = args[0]
        logging.info(f"Short ID received: {short_id}")

        # Check if the user is in required channels
        if not await is_user_in_channels(user_id, app):
            # Dynamically create buttons for each required channel
            keyboard = []
            for channel in REQUIRED_CHANNELS:
                keyboard.append([InlineKeyboardButton(f"Join {channel}", url=f"https://t.me/{channel[1:]}")])  # Remove '@' from channel name

            # Add the Retry button at the bottom
            keyboard.append([InlineKeyboardButton("Retry", callback_data=f"retry_{short_id}")])
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the error message with the buttons
            await update.message.reply_text(
                "❌ You must join the required channels to access this feature.\n\n"
                "Please join the channels below and then click 'Retry' to receive the file.",
                reply_markup=reply_markup
            )
            return

        # Look up the file_id in the database
        file_id = get_file_id(short_id)
        if file_id:
            logging.info(f"File ID found: {file_id}")

            try:
                # Send a warning message
                warning_message = await update.message.reply_text(
                    "⚠️ Attention! ⚠️\n\n"
                    "🚨 Your file will be automatically deleted in 60 seconds! 🚨\n\n"
                    "To keep your file, please forward it or download and save to downloads, within the time limit. "
                    "If the file gets deleted, you can re-download it, and your download progress will be saved "
                    "just click on the file link again from the channel📥💾\n\n"
                    "Act now to secure your file! ⏳🔐",
                    parse_mode="Markdown"
                )

                # Send the file
                file_message = await update.message.reply_document(document=file_id)
                logging.info(f"File sent successfully: {file_id}")

                # Schedule deletion in the background
                asyncio.create_task(delete_messages_after_delay(
                    context.bot,
                    update.message.chat_id,
                    warning_message.message_id,
                    file_message.message_id
                ))

            except BadRequest as e:
                logging.error(f"Error deleting message: {e}")
                await update.message.reply_text("❌ Failed to delete the file. The message may already be removed.")
        else:
            await update.message.reply_text("❌ Invalid link. The file ID could not be found.")
            logging.warning(f"Short ID not found in database: {short_id}")
    else:
        await update.message.reply_text("❌ No data received in the deep link.")
        logging.warning("No args received in /start command.")

# Callback query handler for the retry button
async def handle_retry(update, context):
    user_id = update.callback_query.from_user.id
    app = context.application

    # Extract the short_id from the callback data
    short_id = update.callback_query.data.split("_")[1] if "_" in update.callback_query.data else None
    if not short_id:
        await update.callback_query.answer("❌ Invalid link. Please try again with a valid deep link.")
        return

    # Log the retry attempt
    logging.info(f"User {user_id} clicked the Retry button for short_id: {short_id}")

    # Check if the user is in required channels
    if not await is_user_in_channels(user_id, app):
        # If still not a member, notify the user
        await update.callback_query.answer("❌ You are still not a member of the required channels.")
        return

    # User is now a member, proceed with the file download
    await update.callback_query.answer("✅ Membership verified! Sending the file...")

    # Look up the file_id in the database
    file_id = get_file_id(short_id)
    if file_id:
        try:
            # Send a warning message
            warning_message = await update.callback_query.message.reply_text(
                "⚠️ Attention! ⚠️\n\n"
                "🚨 Your file will be automatically deleted in 60 seconds! 🚨\n\n"
                "To keep your file, please forward it or download and save to downloads, within the time limit. "
                "If the file gets deleted, you can re-download it, and your download progress will be saved "
                "just click on the file link again from the channel📥💾\n\n"
                "Act now to secure your file! ⏳🔐",
                parse_mode="Markdown"
            )

            # Send the file
            file_message = await update.callback_query.message.reply_document(document=file_id)
            logging.info(f"File sent successfully: {file_id}")

            # Schedule deletion in the background
            asyncio.create_task(delete_messages_after_delay(
                context.bot,
                update.callback_query.message.chat_id,
                warning_message.message_id,
                file_message.message_id
            ))

        except BadRequest as e:
            logging.error(f"Error deleting message: {e}")
            await update.callback_query.message.reply_text("❌ Failed to delete the file. The message may already be removed.")
    else:
        await update.callback_query.message.reply_text("❌ Invalid link. The file ID could not be found.")
        logging.warning(f"Short ID not found in database: {short_id}")

# Background task to delete messages after a delay
async def delete_messages_after_delay(bot, chat_id, warning_message_id, file_message_id):
    try:
        # Wait for 60 seconds
        await asyncio.sleep(60)

        # Delete the file message
        await bot.delete_message(chat_id=chat_id, message_id=file_message_id)
        logging.info(f"File message deleted: {file_message_id}")

        # Delete the warning message
        await bot.delete_message(chat_id=chat_id, message_id=warning_message_id)
        logging.info(f"Warning message deleted: {warning_message_id}")

    except BadRequest as e:
        logging.error(f"Error deleting message: {e}")