from pyrogram import Client, filters

from texttospeech.db.models import *
from ... import handlers


@Client.on_message(filters.new_chat_members, group=handlers.NEW_CHAT_MEMBERS)
async def on_new_chat_members(_, message):
    for member in message.new_chat_members:
        if member.is_self:
            message.self_was_added = True
            continue

        User.from_pyrogram(member)
