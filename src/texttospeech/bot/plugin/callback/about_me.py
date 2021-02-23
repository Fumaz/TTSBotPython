from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from texttospeech.bot import cfilters


def create_keyboard(user) -> InlineKeyboardMarkup:
    menu = user.get_message('menu_button')

    return InlineKeyboardMarkup([[InlineKeyboardButton(menu, callback_data='main_menu')]])


@Client.on_callback_query(cfilters.callback_data("info"))
async def on_about_me(_, callback):
    user = callback.db_user

    await callback.answer()
    await callback.edit_message_text(user.get_message("about_me"), reply_markup=create_keyboard(user),
                                     disable_web_page_preview=True)
