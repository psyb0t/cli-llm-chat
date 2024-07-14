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
ENV_VAR_TELEGRAM_BOT_SUPERUSER_CHAT_ID: str = "TELEGRAM_BOT_SUPERUSER_CHAT_ID"

# File to store user data
USER_DATA_FILE: str = os.getenv(ENV_VAR_TELEGRAM_BOT_USER_DATA_FILE, "")
if not USER_DATA_FILE:
    raise ValueError("TELEGRAM_BOT_USER_DATA_FILE environment variable not set")

# Superuser chat ID
SUPERUSER_CHAT_ID: str = os.getenv(ENV_VAR_TELEGRAM_BOT_SUPERUSER_CHAT_ID, "")
if not SUPERUSER_CHAT_ID:
    logger.warning("TELEGRAM_BOT_SUPERUSER_CHAT_ID environment variable not set")

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
        await update.message.reply_text("Hello! What's your name?")
        logger.info(f"New user with chat_id {chat_id} started the bot")
        return

    await update.message.reply_text(f"Hello again, {user_data[chat_id]}!")
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
        await update.message.reply_text(f"Thanks! {update.message.text}!")
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


async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id: str = str(update.effective_chat.id)
    command: str = update.message.text.split()[0][1:]
    args: str = (
        update.message.text.split(None, 1)[1]
        if len(update.message.text.split()) > 1
        else ""
    )

    if chat_id == SUPERUSER_CHAT_ID:
        if command in [
            "temp",
            "temperature",
            "max_tokens",
            "top_p",
            "top_k",
            "repetition_penalty",
            "debug",
        ]:
            param = "temperature" if command == "temp" else command
            param = "max_new_tokens" if param == "max_tokens" else param
            chatbot.set_parameter(param, args)
            await update.message.reply_text(
                f"{param.capitalize()} set to: {getattr(chatbot, param)}"
            )
            return
        elif command == "system":
            chatbot.set_parameter("system_message", args)
            await update.message.reply_text(
                f"System message set to: {chatbot.system_message}"
            )
            return
        elif command == "users":
            await send_user_list(update, context)
            return

    if command == "clear":
        chatbot.clear_history()
        await update.message.reply_text("Chat history cleared")
        return
    elif command == "history":
        history = chatbot.history.get(chat_id, [])
        history_text = "\n".join(
            [f"{entry['role'].capitalize()}: {entry['content']}" for entry in history]
        )
        await update.message.reply_text(f"Chat history:\n{history_text}")
        return
    elif command in ["help", "?"]:
        await send_help_message(
            update, context, is_superuser=(chat_id == SUPERUSER_CHAT_ID)
        )
        return
    else:
        await update.message.reply_text(f"Unknown command: {command}")
        return


async def send_help_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, is_superuser: bool
) -> None:
    help_message = "Available commands:\n"
    help_message += "/clear: Clear chat history\n"
    help_message += "/history: Show chat history\n"
    help_message += "/help or /?: Show this help message\n"

    if is_superuser:
        help_message += "\nSuperuser commands:\n"
        help_message += "/temp <value>: Set temperature\n"
        help_message += "/max_tokens <value>: Set max new tokens\n"
        help_message += "/top_p <value>: Set top_p\n"
        help_message += "/top_k <value>: Set top_k\n"
        help_message += "/repetition_penalty <value>: Set repetition penalty\n"
        help_message += "/system <message>: Set system message\n"
        help_message += "/debug true|false: Enable or disable debug mode\n"
        help_message += "/users: Show all users (chat ID and username)\n"

    await update.message.reply_text(help_message)


async def send_user_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != SUPERUSER_CHAT_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    user_list = "User List:\n"
    for chat_id, username in user_data.items():
        user_list += f"Chat ID: {chat_id}, Username: {username}\n"

    await update.message.reply_text(user_list)


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
    application.add_handler(MessageHandler(filters.COMMAND, handle_command))
    logger.info("Handlers added to the application")

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting to poll for updates")
    application.run_polling()


if __name__ == "__main__":
    main()
