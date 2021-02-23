from pyrogram import Client

from texttospeech.db.models import *
from .. import handlers


@Client.on_message(group=handlers.DATABASE)
async def on_message(_, message):
    message.db_user = User.from_pyrogram(message)
    message.db_chat = Chat.from_pyrogram(message)


@Client.on_callback_query(group=handlers.DATABASE)
async def on_callback_query(_, callback):
    callback.db_user = User.from_pyrogram(callback)


@Client.on_inline_query(group=handlers.DATABASE)
async def on_inline_query(_, query):
    query.db_user = User.from_pyrogram(query)


@Client.on_chosen_inline_result(group=handlers.DATABASE)
async def on_chosen_inline_result(_, chosen):
    chosen.db_user = User.from_pyrogram(chosen)
