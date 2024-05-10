from typing import Optional, List

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext


async def location(update: Update, context: CallbackContext):
    user_location = update.message.location
    print(user_location)
    msg_id = update.message.message_id
    context.bot_data['last_bot_message'] = msg_id
    await update.message.reply_text(f"Received location: {user_location.latitude}, {user_location.longitude}")
    return user_location.latitude, user_location.longitude


async def location_possibility(update: Update):
    location_button = KeyboardButton(text="Send your location", request_location=True)
    skip_button = KeyboardButton(text="Choose city")
    custom_keyboard = [[location_button, skip_button]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Please share your location or skip:", reply_markup=reply_markup)

    return await get_user_response(update, ['Send your location', 'Choose city'])


async def get_user_response(update: Update, options: List[str]) -> Optional[str]:
    while True:
        user_message = update.message
        if user_message.text in options:
            return user_message.text.strip()
        break


async def get_last_user_input(update: Update) -> Optional[str]:
    while True:
        # Wait for user message
        user_message = update.message
        if user_message.text:
            return user_message.text.strip()
