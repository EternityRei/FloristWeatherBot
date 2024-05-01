import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from ..agent import Agent


async def handle_message(
        update: Update,
        context: CallbackContext,
        agent: Agent
) -> None:
    user_text = update.message.text
    chat_id = update.message.chat_id
    agent_response = agent.ask(user_text)['output']
    await context.bot.send_message(chat_id=chat_id, text=agent_response)


async def start_command_handler(
        update: Update,
        context: CallbackContext
):
    user_text = update.message.text
    if user_text == '/start':
        chat_id = update.message.chat_id
        response = f""" Hey there! 🌙✨ I'm your Dream Journal Bot. Each morning, I’ll be here to listen to your dreams. 
        \nJust type them in and I'll help you explore patterns and themes over time. Ready to unlock the mysteries of your 
        dreams?\nLet's get started!"""
        await context.bot.send_message(chat_id=chat_id, text=response)
    else:
        agent = Agent()
        await handle_message(update, context, agent)


def main():
    application = Application.builder().token(os.environ.get('BOT_TOKEN')).build()

    text_handler = MessageHandler(filters.TEXT, lambda update, context: start_command_handler(update, context))
    application.add_handler(text_handler)

    application.run_polling()
