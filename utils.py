import logging
import os
from datetime import datetime
from telegram.ext import Application
from config import REQUIRED_CHANNELS
from logging.handlers import RotatingFileHandler

# Function to set up logging
def setup_logging():
    # Create the Log folder if it doesn't exist
    log_folder = "Log"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Generate a log file name with the current date and time
    log_file_name = datetime.now().strftime("log-%Y-%m-%d-%H-%M-%S.txt")
    log_file_path = os.path.join(log_folder, log_file_name)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),  # Log to a file
            logging.StreamHandler()             # Log to the console
        ]
    )

    # Disable httpx INFO logs
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)

    # Add a rotating file handler
    rotating_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3)
    logging.getLogger().addHandler(rotating_handler)

# Function to check if the user is in required channels
async def is_user_in_channels(user_id, app: Application):
    for channel in REQUIRED_CHANNELS:
        try:
            # Log the channel and user ID being checked
            logging.info(f"Checking membership for user {user_id} in channel {channel}")

            # Get chat member details
            chat_member = await app.bot.get_chat_member(chat_id=channel, user_id=user_id)
            logging.info(f"Chat member status: {chat_member.status}")

            # Check if the user is a member, admin, or creator
            if chat_member.status in ["member", "administrator", "creator"]:
                return True
        except Exception as e:
            logging.error(f"Error checking membership in {channel}: {e}")
    return False