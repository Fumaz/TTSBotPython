from pyrogram import Client

from texttospeech.bot import cfilters
from texttospeech.bot.plugin import settings
from texttospeech.db.models import Settings
from texttospeech.util.emojifier import Emoji


@Client.on_callback_query(cfilters.callback_data("toggle_slow_mode"))
async def on_slow_mode(_, callback):
    user = callback.db_user

    slow_mode = Emoji.from_boolean(user.toggle_setting(Settings.SLOW_MODE))
    message = user.get_message('toggle_slow_mode', status=slow_mode)

    await callback.edit_message_text(settings.create_message(user), reply_markup=settings.create_keyboard(user))
    await callback.answer(message, show_alert=True)
