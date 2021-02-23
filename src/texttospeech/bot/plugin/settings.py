from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from texttospeech.bot import cfilters
from texttospeech.db.models import *


@db_session
def create_message(user) -> str:
    always_speak = user.get_setting(Settings.ALWAYS_SPEAK, Emoji)
    slow_mode = user.get_setting(Settings.SLOW_MODE, Emoji)
    language = user.get_message('full_name')

    return user.get_message('settings_message',
                            always_speak=always_speak,
                            slow_mode=slow_mode,
                            language=language)


@db_session
def create_keyboard(user) -> InlineKeyboardMarkup:
    always_speak = user.get_setting(Settings.ALWAYS_SPEAK, Emoji)
    slow_mode = user.get_setting(Settings.SLOW_MODE, Emoji)

    always_speak_button = InlineKeyboardButton(user.get_message('always_speak_button', status=always_speak),
                                               callback_data='toggle_always_speak')

    slow_mode_button = InlineKeyboardButton(user.get_message('slow_mode_button', status=slow_mode),
                                            callback_data='toggle_slow_mode')

    language_button = InlineKeyboardButton(user.get_message('language_button'),
                                           callback_data='change_language')

    menu_button = InlineKeyboardButton(user.get_message('menu_button'),
                                       callback_data='main_menu')

    return InlineKeyboardMarkup([[always_speak_button, slow_mode_button], [language_button], [menu_button]])


@Client.on_message(filters.command('settings') & filters.private)
async def on_settings_command(_, message):
    user = message.db_user

    await message.reply_text(create_message(user), reply_markup=create_keyboard(user))


@Client.on_callback_query(cfilters.callback_data('settings'))
async def on_settings_callback(_, callback):
    user = callback.db_user

    await callback.answer()
    await callback.edit_message_text(create_message(user), reply_markup=create_keyboard(user))
