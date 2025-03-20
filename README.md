# **tg-simple-file-bot**

![License](https://img.shields.io/badge/license-GPLv3-blue.svg) ![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)

**tg-simple-file-bot** is a lightweight Telegram bot designed for simple file uploads and downloads. Built with Python and powered by SQLite for local storage, this bot is perfect for users looking for a minimalistic solution to share files via Telegram. The project is optimized to run locally on Termux, making it accessible for Android users without requiring advanced configurations.

---

## **Features**

- **File Uploads**: Upload single files (documents, photos, videos) to the bot.
- **File Downloads**: Retrieve uploaded files using unique links.
- **SQLite Database**: Stores file metadata locally for quick access.
- **Lightweight**: Minimal dependencies and easy to set up.
- **Termux-Compatible**: Designed to run seamlessly on Termux for Android users.

---

## **Requirements**

- Python 3.8 or higher
- A Telegram Bot Token (obtained from [BotFather](https://core.telegram.org/bots#botfather))
- SQLite (included in Python's standard library)
- Termux (optional, for Android users)

---

## **Installation**

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/estiaksoyeb/tg-simple-file-bot.git
cd tg-simple-file-bot
```

### **Step 2: Install Dependencies**

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```


### **Step 3: Configure the Bot**

To configure the bot, edit the `config.py` file in the project directory. Follow these steps:

1. Open the `config.py` file in your preferred text editor.
2. Update the following fields with your bot's details:

   ```python
   # Bot Token
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

   # Bot Username
   BOT_USERNAME = "YOUR_BOT_USERNAME_HERE"

   # Required Channels for Access
   REQUIRED_CHANNELS = ["@YOUR_CHANNEL_USERNAME_HERE"]
   ```

   - Replace `YOUR_BOT_TOKEN_HERE` with the token you received from [BotFather](https://core.telegram.org/bots#botfather).
   - Replace `YOUR_BOT_USERNAME_HERE` with the username of your bot (e.g., `your_bot_username` without the `@` symbol).
   - Replace `@YOUR_CHANNEL_USERNAME_HERE` with the username(s) of the required channel(s) that users must join to access the bot.

   > **Note**: Ensure that the `BOT_TOKEN` and channel usernames are accurate. Incorrect values may cause the bot to malfunction.


### **Example Configuration**

Here’s an example of what your `config.py` file might look like after configuration:

```python
# Bot Token
BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRstuVWXyz"

# Bot Username
BOT_USERNAME = "example_bot"

# Required Channels for Access
REQUIRED_CHANNELS = ["@required_channel"]
```

---

### **Step 4: Run the Bot**

Start the bot by running the following command:

```bash
python main.py
```

The bot will start polling for updates and is ready to handle file uploads and downloads.

---

## **Usage**

1. **Upload a File**:
   - Send a document, photo, or video to the bot.
   - The bot will generate a unique download link for the file.

2. **Download a File**:
   - Click the generated link or use the `/start` command with the file's `short_id` to retrieve the file.

---

## **Database**

The bot uses SQLite for storing file metadata locally. The database file (`bot_database.db`) will be created automatically when you run the bot for the first time.

---

## **Contributing**

Contributions are welcome! If you’d like to improve this project, feel free to fork the repository and submit a pull request. Please ensure your changes align with the project's simplicity and focus on functionality.

> **Important**: This project is licensed under the **GNU General Public License v3.0**, which means any derivative works must also be licensed under the GPL. Always respect the terms of the license when contributing.

---

## **License**

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for more details.

---

## **Acknowledgments**

- Thanks to the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library for making Telegram bot development easier.
- Inspired by the simplicity of file-sharing bots on Telegram.

---

## **Disclaimer**

This project is intended for educational and personal use only. The developer is not responsible for any misuse or damages caused by the bot.
