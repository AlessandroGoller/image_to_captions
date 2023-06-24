""" Telegram """

import time
import traceback
from typing import Optional

from aiogram import Bot, Dispatcher, types

from app.crud.company import get_company_by_user_id
from app.crud.instagram import get_last_n_instagram
from app.crud.telegram import (
    create_telegram,
    delete_telegram,
    get_prompt_by_id_chat,
    get_telegram_by_chat_id,
    update_last_access,
    update_message_description,
    update_message_prompt,
)
from app.crud.user import get_user_by_hash
from app.dependency import get_settings
from app.model.company import Company
from app.model.user import User
from app.schema.telegram import TelegramCreate
from app.services.langchain import (
    generate_ig_post,
    generate_img_description,
)
from app.utils.logger import configure_logger
from app.utils.openai.prompt import create_prompt
from app.utils.telegram_utils import check_chat

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

list_commands_inline_basic_message = [
    {"command": "/start_test", "label": "Avvia Inline"},
    {"command": "/help_inline", "label": "Aiuto Inline"},
    {"command": "/profile", "label": "Modifica il Profilo"}
]

list_commands_inline_action = [
    {"command": "/ok_action_post", "label": "OK"},
    {"command": "/home_action_post", "label": "HOME"},
]

list_commands_after_prompt = [
    {"command": "/prompt_1", "label": "1"},
    {"command": "/prompt_2", "label": "2"},
    {"command": "/prompt_3", "label": "3"},
]

list_commands_after_selected_prompt = [
    {"command": "/edit_result", "label": "Modifica il risultato"},
    {"command": "/home", "label": "Home"},
]

def create_inline_keyboard(list_command: list[dict])-> types.InlineKeyboardMarkup:
    """ Permit to create the inline comands for telegram"""
    keyboard = []
    for cmd in list_command:
        button = types.InlineKeyboardButton(text=cmd["label"], callback_data=cmd["command"])
        keyboard.append([button])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.callback_query_handler()
async def handle_callback_query(query: types.CallbackQuery)->str:
    """ Handle the keyboard query pression """
    # bisogna aggiungere una verifica anche qua per sicurezza
    button_data = query.data
    if button_data == "/help_inline":
        await bot.edit_message_text("Help page",
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                reply_markup=None)
    elif button_data == "/start_test":
        await bot.edit_message_text("Avvia Inline, attivato",
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                reply_markup=None)
        await action_post(query.message)
    elif button_data =="/profile":
        await bot.edit_message_text("Modifica il Profilo, attivato",
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                reply_markup=None)
        await profile_settings(query.message)
    elif button_data =="/ok_action_post":
        await bot.edit_message_text("Se tutto andasse ora potresti caricare una immagine",
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                reply_markup=None)
    elif button_data=="ciao":
        await bot.edit_message_text(f"Hello! user_full_name\nIl tuo messaggio è: {query.message.text}",
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=None)
    elif button_data in ["/prompt_1","/prompt_2","/prompt_3"]:
        try:
            full_prompt:str = get_prompt_by_id_chat(query.message.chat.id)
            selected_prompt_list = full_prompt.split("Post")
            if button_data=="/prompt_1":
                selected_prompt = selected_prompt_list[0]
            elif button_data=="/prompt_2":
                selected_prompt = selected_prompt_list[1]
            elif button_data=="/prompt_3":
                selected_prompt = selected_prompt_list[2]
            else:
                selected_prompt = selected_prompt_list[0]
            await bot.edit_message_text(f"Post selezionato: \n\n{selected_prompt}",
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                reply_markup=None)
            update_message_prompt(id_chat=query.message.chat.id, prompt=selected_prompt)
        except Exception as error:
            logger.error(
                f"ERROR during choose of the prompt: {error}\n{traceback}"
            )
            await bot.edit_message_text(f"There was an error: {error}\n-----\n{traceback}",
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                reply_markup=None)
    elif button_data in [item["command"] for item in list_commands_after_selected_prompt]:
        try:
            if button_data == "/edit_result":
                await bot.edit_message_text("Al momento questa funzione non è disponibile",
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                    reply_markup=None)
            else:
                prompt:str = get_prompt_by_id_chat(query.message.chat.id)
                await bot.edit_message_text(prompt,
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                    reply_markup=None)
        except Exception as error:
            logger.error(
                f"ERROR during choose if edit or not: {error}\n{traceback}"
            )
            await bot.edit_message_text(f"There was an error: {error}\n-----\n{traceback}",
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
    if telegram is not None and telegram.id_user != user.user_id:
        delete_telegram(telegram)
        telegram_schema = TelegramCreate(
            id_user=user.user_id,
            id_user_telegram=int(message.from_user.id),
            id_chat=int(message.chat.id)
        )
        telegram = create_telegram(telegram=telegram_schema)
    else:
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
    """ Anwser message for all messages  """
    try:
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logger.info(f"Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}")

        telegram = check_chat(message.chat.id)
        if telegram is False:
            await message.reply(f"Hello!{user_full_name=}\nPer favore fai il primo accesso via browser")
            return "ok"
        update_last_access(telegram.id_telegram)
        await message.answer(f"Hello!{user_full_name=}\nIl tuo messaggio è:{message.text}",
                reply_markup=create_inline_keyboard(list_commands_inline_basic_message))
        return "ok"
    except Exception as error:
        logger.info(f"Main: {user_id} {user_full_name} {time.asctime()}.\
                    Message: {message}. Error in main_handler\n {error}")
        await message.reply("Something went wrong...")
        return f"There was an error: {error}"

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def image_handler(message: types.Message)->str:
    """ Anwser message only for images """
    telegram = check_chat(message.chat.id)
    if telegram is False:
        await message.reply(f"Hello!{message.from_user.full_name}\nPer favore fai il primo accesso via browser",
                                reply_markup=None)
        return "No account"
    image = message.photo[-1]
    try:
        await message.reply("Stiamo preparando il tutto")
        file_id = image.file_id
        # Recupera l'oggetto immagine utilizzando il file_id
        file = await bot.get_file(file_id)
        # Scarica il contenuto dell'immagine come byte array
        image_bytes = await bot.download_file(file.file_path)

        description_image: str = generate_img_description(image_bytes)
        await message.reply(f"Descrizione dell'immagine: {description_image}")
        update_message_description(id_chat=message.chat.id, description=description_image)
        company: Optional[Company] = get_company_by_user_id(user_id=telegram.id_user)
        if company is None:
            await message.reply("Please go to website and add IG user")
            return "No company"
        sample_posts = get_last_n_instagram(
                company_id=company.id_company, number_ig=20
            )
        await message.reply("Extracted instagram images from db")
        prompt:str = create_prompt(sample_posts, description_image)
        posts = generate_ig_post(telegram.user.email, prompt)
        all_posts = ""
        for i, post in enumerate(posts):
            all_posts += f"Post {i+1}):\n{post}\n\n"
        all_posts_reply = all_posts + "\n-------\nQuale Post vuoi tenere?"
        await message.reply(f"{all_posts_reply}",
            reply_markup=create_inline_keyboard(list_commands_after_prompt))
        update_message_prompt(id_chat=message.chat.id, prompt=all_posts)
        await message.reply(f"messaggio salvato: {get_prompt_by_id_chat(id_chat=message.chat.id)}")
    except Exception as error:
        logger.error(
            f"ERROR during action from telegram{error}\n{traceback}"
        )
        await message.reply(f"There was an error: {error}\n-----\n{traceback}")
    return "ok"


async def profile_settings(message: types.Message)->None:
    """
    Shows the profile settings

    Parameters
    ----------
    message : types.Message
    """
    telegram = check_chat(message.chat.id)
    if telegram is False:
        await message.reply(f"Hello!{message.from_user.full_name}\nPer favore fai il primo accesso via browser",
                                        reply_markup=None)
        return

    try:
        profile_settings_text = f"Email: {telegram.user.email}\n \
                            name: {telegram.user.name}\n \
                            password: Non la sappiamo neache noi :)\n \
                            Lingua: {telegram.user.language}\n \
                            last_access: {telegram.user.last_access}\n \
                            time_created: {telegram.user.time_created}\n \
                            Tokens da pagare: {telegram.user.tokens_to_be_paid}\n \
                            Totale Tokens: {telegram.user.total_tokens}"

        await message.reply(f"DOVRESTI ESSERE in Settings!! =\n{profile_settings_text}",
        reply_markup=None)

    except Exception as error:
        logger.error(
            f"ERROR during profile settings {error}\n{traceback}"
        )
        await message.reply(f"There was an error: {error}\n-----\n{traceback}")


async def action_post(message: types.Message) -> None:
    """
    action_post

    Parameters
    ----------
    message : types.Message
    """
    telegram = check_chat(message.chat.id)
    if telegram is False:
        await message.reply(f"Hello!{message.from_user.full_name}\nPer favore fai il primo accesso via browser",
                                reply_markup=None)
        return
    keyboard = []
    for cmd in list_commands_inline_action:
        button = types.InlineKeyboardButton(text=cmd["label"], callback_data=cmd["command"])
        keyboard.append([button])
    command_inline = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.reply("DOVRESTI ESSERE in ACTION!! =\n",
                                reply_markup=command_inline)
