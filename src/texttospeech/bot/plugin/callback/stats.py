from datetime import timedelta

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from texttospeech.bot import cfilters
from texttospeech.db.models import *


def create_keyboard(user) -> InlineKeyboardMarkup:
    menu = user.get_message('menu_button')

    return InlineKeyboardMarkup([[InlineKeyboardButton(menu, callback_data='main_menu')]])


@Client.on_callback_query(cfilters.callback_data("stats"))
async def on_stats(_, callback):
    if not callback.db_user.is_admin:
        await callback.answer(text='N/A', show_alert=True)
        return

    with db_session:
        user = callback.db_user
        users = User.select().count()
        groups = Chat.select().count()
        audios = Audio.select().count()

        users_today = User.select(lambda u: u.creation_date >= (datetime.now() - timedelta(hours=24))).count()
        groups_today = Chat.select(lambda c: c.creation_date >= (datetime.now() - timedelta(hours=24))).count()
        audios_today = Audio.select(lambda a: a.creation_date >= (datetime.now() - timedelta(hours=24))).count()
        active_users = User.select(lambda u: u.last_update >= (datetime.now() - timedelta(hours=24))).count()

        await callback.answer()
        await callback.edit_message_text(user.get_message("stats_message", users=users, groups=groups, audios=audios,
                                                          users_today=users_today, groups_today=groups_today,
                                                          audios_today=audios_today, active_users=active_users),
                                         reply_markup=create_keyboard(user))
