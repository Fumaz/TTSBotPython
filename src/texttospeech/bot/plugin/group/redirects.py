from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from texttospeech.bot import cfilters
from texttospeech.util import formatting


async def reply_redirect(message, deeplink):
    user = message.db_user

    msg = user.get_message('group_redirect_message')
    button = user.get_message('group_redirect_button')

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button, url=formatting.deeplink(deeplink))]])

    await message.reply_text(msg, reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_message(filters.group & cfilters.group_command('settings'))
async def on_settings_command(_, message):
    await reply_redirect(message, 'settings')


@Client.on_message(filters.group & cfilters.group_command('language'))
async def on_language_command(_, message):
    await reply_redirect(message, 'language')


@Client.on_message(filters.group & cfilters.group_command('start'))
async def on_start_command(_, message):
    if 'added' in message.command:
        return

    await reply_redirect(message, 'start')
