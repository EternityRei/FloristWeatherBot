import os
from typing import Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from ..agent import Agent
from .stt_handler import transcribe_audio
from fwbot.util.utils import location_possibility, location, get_last_user_input
from langchain.tools import tool
from langchain_core.messages import HumanMessage


async def handle_message(
        update: Update,
        context: CallbackContext,
        custom_text: Optional[str] = None
) -> None:
    user_text = custom_text if custom_text is not None else update.message.text
    chat_id = update.message.chat_id
    ask_for_location = [False]

    @tool
    def create_buttons_for_user_to_share_location():
        """
        Used to ask their location to get the weather, used just after user asked about weather.
        Always use this function when you ask for user location for weather.
        """
        ask_for_location[0] = True

    agent = Agent(additional_tools=[create_buttons_for_user_to_share_location])
    agent_response = agent.ask(prompt=user_text, chat_history=context.user_data.get('chat_history', []))['output']

    if update.message.location:
        lat, lon = await location(update, context)
        user_text = f'{lat}°N, {lon}°W'
        agent_response = agent.ask(prompt=user_text, chat_history=context.user_data.get('chat_history', []))['output']
        await context.bot.send_message(chat_id=chat_id, text=agent_response)
        context.user_data['state'] = False
    elif context.user_data.get('state', False) == 'waiting_for_answer':
        result = update.message.text
        if result == 'Choose city':
            context.user_data['state'] = 'waiting_for_city'
            await context.bot.send_message(chat_id=chat_id, text=agent_response)
        else:
            context.user_data['state'] = 'waiting_for_answer'
            await context.bot.send_message(chat_id=chat_id, text="Please choose your option")
    elif ask_for_location[0]:
        await location_possibility(update)
        context.user_data['state'] = 'waiting_for_answer'
    elif context.user_data.get('state', False) == 'waiting_for_city':
        context.user_data['state'] = False
        await context.bot.send_message(chat_id=chat_id, text=agent_response)
    else:
        await context.bot.send_message(chat_id=chat_id, text=agent_response)
    chat_history = context.user_data.get('chat_history', [])
    chat_history.append(HumanMessage(content=user_text))
    chat_history.append(agent_response)
    context.user_data['chat_history'] = chat_history


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
    # await location_possibility(update)


def main():
    application = Application.builder().token(os.environ.get('BOT_TOKEN')).build()

    start_handler = CommandHandler('start', lambda update, context: start_command_handler(update, context))
    text_handler = MessageHandler(filters.TEXT, lambda update, context: handle_message(update, context))
    voice_handler = MessageHandler(filters.VOICE, lambda update, context: voice_handle(update, context))

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(voice_handler)
    application.add_handler(MessageHandler(filters.LOCATION, lambda update, context: handle_message(update, context)))

    application.run_polling()
