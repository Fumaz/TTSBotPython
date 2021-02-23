from pyrogram import Client, filters

from texttospeech.db.models import *
from ... import handlers


@Client.on_message(filters.migrate_from_chat_id, group=handlers.MIGRATION)
async def on_migrate_from_chat_id(_, message):
    message.db_chat.set_setting(Settings.WELCOME_SENT, True)


@Client.on_message(filters.migrate_to_chat_id, group=handlers.MIGRATION)
async def on_migrate_to_chat_id(_, message):
    with db_session:
        message.db_chat.current.delete()
