""" Telegram """

import time
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.crud.telegram import create_telegram, delete_telegram, get_telegram_by_chat_id, update_last_access
from app.crud.user import get_user_by_hash
from app.dependency import get_settings
from app.model.user import User
from app.schema.telegram import TelegramCreate
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

# Telegram settings
WEBHOOK_URL = settings.DOMAIN + settings.WEBHOOK_PATH
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

commands = [
        types.BotCommand(command="/help", description="Show help"),
        types.BotCommand(command="/bomba", description="Explodeeee")
    ]

list_commands_inline = [
    {'command': '/start_test', 'label': 'Avvia Inline'},
    {'command': '/help_inline', 'label': 'Aiuto Inline'},
    {'command': '/info', 'label': 'Informazioni Inline'}
]

def create_inline_keyboard()-> types.InlineKeyboardMarkup:
    """ Permit to create the inline comands for telegram"""
    keyboard = []
    for cmd in list_commands_inline:
        button = types.InlineKeyboardButton(text=cmd['label'], callback_data=cmd['command'])
        keyboard.append([button])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.callback_query_handler()
async def handle_callback_query(query: types.CallbackQuery)->str:
    """ Handle the keyboard query pression """
    button_data = query.data

    if button_data == 'start_test':
        await bot.answer_callback_query(query.id, text='Hai selezionato il pulsante start_test')
    elif button_data == '/start_test':
        await bot.answer_callback_query(query.id, text='Hai selezionato il pulsante /start_test 2')
    else:
        await bot.answer_callback_query(query.id, text='Pulsante non valido')

    await bot.edit_message_text(f"Hello! user_full_name\nIl tuo messaggio è: {query.message.text}",
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                reply_markup=None)
    return "ok"


@dp.message_handler(commands="help")
async def help_comand(message: types.Message)->str:
    """ Anwser message for commands start """
    await message.answer("NON fa nulla2 :)")
    return "ok"

@dp.message_handler(commands="bomba")
async def info_comand(message: types.Message)->str:
    """ Anwser message for commands start """
    await message.answer("NON fa nulla 3:)")
    return "ok"

@dp.message_handler(commands="start")
async def start(message: types.Message)->str:
    """ Anwser message for commands start """
    hash_code: str = message.text.split(" ")
    if len(hash_code)<=1:
        await message.answer(f"Error hash code, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}")
        return "ok"
    hash_code = hash_code[1]
    user: Optional[User] = get_user_by_hash(hash_code=hash_code)
    if user is None:
        await message.answer(f"Salom, {message.from_user.full_name}\n \
                            Impossible to find account, try again")
        return "ok, but with impossible account"
    telegram = get_telegram_by_chat_id(message.chat.id)
    if telegram is not None:
        if telegram.id_user == user.user_id:
            update_last_access(telegram.id_telegram)
            await message.answer(f"Salom another time, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}\n{telegram.user.email}")
            return "ok"
        delete_telegram(telegram)
    telegram_schema = TelegramCreate(
        id_user=user.user_id,
        id_user_telegram=int(message.from_user.id),
        id_chat=int(message.chat.id)
    )
    telegram = create_telegram(telegram=telegram_schema)
    update_last_access(telegram)
    await message.answer(f"Salom, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}\n{telegram.user.email}")
    await message.answer(f"Telegram row created:, {telegram.id_user}\n{telegram.id_chat=}\n\
                        {telegram.id_user_telegram=}")
    return "ok"

@dp.message_handler()
async def main_handler(message: types.Message)-> str:
    """ Anwser message for other commands """
    try:
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logger.info(f"Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}")

        telegram = get_telegram_by_chat_id(message.chat.id)
        if telegram is None:
            await message.reply(f"Hello!{user_full_name=}\nPer favore fai il primo accesso via browser")
            return "ok"
        update_last_access(telegram.id_telegram)
        await message.reply(f"Hello!{user_full_name=}\nIl tuo messaggio è:{message.text}",reply_markup=create_inline_keyboard())
        return "ok"
    except Exception as error:
        logger.info(f"Main: {user_id} {user_full_name} {time.asctime()}.\
                    Message: {message}. Error in main_handler\n {error}")
        await message.reply("Something went wrong...")
        return f"There was an error: {error}"
