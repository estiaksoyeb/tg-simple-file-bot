from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from database import init_database
from file_handlers import handle_file_upload
from start_handler import start, handle_retry
from utils import setup_logging
from config import BOT_TOKEN

# Main function to run the bot
def main():
    # Initialize logging
    setup_logging()

    # Initialize the database
    init_database()

    # Start the bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_file_upload))
    app.add_handler(CallbackQueryHandler(handle_retry))  # Add the retry button handler

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()