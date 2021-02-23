from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texttospeech.bot import cfilters
from texttospeech.db.models import Settings
from texttospeech.localization import languages
from texttospeech.util import formatting


@Client.on_message(filters.group & ((~cfilters.group_setting(Settings.WELCOME_SENT)) | cfilters.added))
async def on_send_welcome(_, message):
    language = 'en_US'

    if message.db_user:
        language = message.db_user.language

    message.db_chat.set_setting(Settings.WELCOME_SENT, True)
    msg = languages.get_message('group_self_was_added', language)

    await message.reply_text(msg, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(languages.get_message('inline_create_audio', language),
                              switch_inline_query_current_chat='')],
        [InlineKeyboardButton(languages.get_message('settings_button', language),
                              url=formatting.deeplink('settings'))]
    ]))
