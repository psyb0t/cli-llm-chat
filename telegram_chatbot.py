import os
import json
import logging
from chat import Chatbot
from time import sleep
from random import uniform
from typing import Dict
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Constants for environment variable names
ENV_VAR_TELEGRAM_BOT_TOKEN: str = "TELEGRAM_BOT_TOKEN"
ENV_VAR_TELEGRAM_BOT_USER_DATA_FILE: str = "TELEGRAM_BOT_USER_DATA_FILE"

# File to store user data
USER_DATA_FILE: str = os.getenv(ENV_VAR_TELEGRAM_BOT_USER_DATA_FILE, "")
if not USER_DATA_FILE:
    raise ValueError("TELEGRAM_BOT_USER_DATA_FILE environment variable not set")

# Dictionary to store chat_id: username pairs
user_data: Dict[str, str] = {}

# Initialize the AI chatbot global var
chatbot: Chatbot | None = None


# Load user data from file
def load_user_data() -> None:
    global user_data
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            user_data = json.load(f)
        logger.info(f"Loaded user data from {USER_DATA_FILE}")
        return
    logger.warning(
        f"User data file {USER_DATA_FILE} not found. Starting with empty user data."
    )


# Save user data to file
def save_user_data() -> None:
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f)
    logger.debug(f"Saved user data to {USER_DATA_FILE}")


# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id: str = str(update.effective_chat.id)
    if chat_id not in user_data:
        await update.message.reply_text("eyo! CUM te cheama?")
        logger.info(f"New user with chat_id {chat_id} started the bot")

        return

    await update.message.reply_text(f"cetzma plashipula, {user_data[chat_id]}!")
    logger.info(
        f"Existing user {user_data[chat_id]} (chat_id: {chat_id}) started the bot"
    )


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id: str = str(update.effective_chat.id)

    logger.debug(f"Received message from chat_id: {chat_id}: {update.message.text}")

    if chat_id not in user_data:
        user_data[chat_id] = update.message.text
        save_user_data()
        await update.message.reply_text(f"tzumesque! {update.message.text}! 🐟🐟🐟")
        logger.info(f"New user registered: {update.message.text} (chat_id: {chat_id})")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    response = chatbot.generate_response(
        update.message.text,
        user_id=chat_id,
        print_response=False,
    )

    lines = response.split("\n")

    for c, line in enumerate(lines):
        await update.message.reply_text(line)

        if c < len(lines) - 1:
            await context.bot.send_chat_action(
                chat_id=chat_id, action=ChatAction.TYPING
            )
            sleep(uniform(0.2, 1))

    logger.debug(
        f"Answered message for user {user_data[chat_id]} (chat_id: {chat_id}): {response}"
    )


def main() -> None:
    logger.info("Starting the bot")

    telegram_bot_token: str = os.getenv(ENV_VAR_TELEGRAM_BOT_TOKEN, "")
    if not telegram_bot_token:
        logger.fatal(f"Environment variable {ENV_VAR_TELEGRAM_BOT_TOKEN} not set")
        return

    global chatbot
    chatbot = Chatbot()

    # Load existing user data
    load_user_data()

    # Create the Application and pass it your bot's token
    application: Application = Application.builder().token(telegram_bot_token).build()
    logger.info("Application built successfully")

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    logger.info("Handlers added to the application")

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting to poll for updates")
    application.run_polling()


if __name__ == "__main__":
    main()
