import os
from typing import Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from ..agent import Agent
from .stt_handler import transcribe_audio


async def handle_message(
        update: Update,
        context: CallbackContext,
        custom_text: Optional[str] = None
) -> None:
    agent = Agent()
    user_text = custom_text if custom_text is not None else update.message.text
    print(user_text)
    chat_id = update.message.chat_id
    agent_response = agent.ask(user_text)['output']
    await context.bot.send_message(chat_id=chat_id, text=agent_response)


async def voice_handle(update: Update, context: CallbackContext):
    file = await update.message.voice.get_file()
    text = await transcribe_audio(file)
    await handle_message(update, context, custom_text=text)


async def start_command_handler(
        update: Update,
        context: CallbackContext
):
    user_text = update.message.text
    chat_id = update.message.chat_id
    response = ("🌼 Hello and welcome to FloristWeatherBot! I'm here to help you blend the beauty of flowers with the "
                "whimsy of the weather. Whether you're planning a garden, looking for the best blooms for the current "
                "climate, or just curious about today's forecast, I've got you covered with AI-powered insights. "
                "Let's make every day a blooming success! 🌦️🌹")
    await context.bot.send_message(chat_id=chat_id, text=response)


def main():
    application = Application.builder().token(os.environ.get('BOT_TOKEN')).build()

    start_handler = CommandHandler('start', lambda update, context: start_command_handler(update, context))
    text_handler = MessageHandler(filters.TEXT, lambda update, context: handle_message(update, context))
    voice_handler = MessageHandler(filters.VOICE, lambda update, context: voice_handle(update, context))

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(voice_handler)

    application.run_polling()
