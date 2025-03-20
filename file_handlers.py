import hashlib
from database import store_file_id
from config import BOT_USERNAME

# Function to generate a short ID
def generate_short_id(file_id):
    # Use a hash function to generate a 6-character ID
    return hashlib.md5(file_id.encode()).hexdigest()[:6]

# Function to handle file uploads and generate deep links
async def handle_file_upload(update, context):
    file = None

    if update.message.document:
        file = update.message.document.file_id
    elif update.message.video:
        file = update.message.video.file_id
    elif update.message.photo:
        file = update.message.photo[-1].file_id  # Get highest resolution

    if file:
        # Generate a short ID
        short_id = generate_short_id(file)
        store_file_id(short_id, file)  # Store in database

        # Generate bot link
        bot_link = f"https://t.me/{BOT_USERNAME}?start={short_id}"

        # Send the file_id and bot link
        await update.message.reply_text(
            f"✅ **Your file ID:**\n`{file}`\n\n"
            f"🔗 **Download Link:**\n[{bot_link}]({bot_link})\n\n"
            f"Share this link to allow users to download the file.",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text("❌ Please send a document, video, or photo.")