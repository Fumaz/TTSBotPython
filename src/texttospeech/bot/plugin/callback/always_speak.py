from pyrogram import Client

from texttospeech.bot import cfilters
from texttospeech.bot.plugin import settings
from texttospeech.db.models import Settings
from texttospeech.util.emojifier import Emoji


@Client.on_callback_query(cfilters.callback_data("toggle_always_speak"))
async def on_always_speak(_, callback):
    user = callback.db_user

    always_speak = Emoji.from_boolean(user.toggle_setting(Settings.ALWAYS_SPEAK))
    message = user.get_message('toggle_always_speak', status=always_speak)

    await callback.edit_message_text(settings.create_message(user), reply_markup=settings.create_keyboard(user))
    await callback.answer(message, show_alert=True)
