import os

from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from texttospeech.audio import tts
from texttospeech.bot import cfilters
from texttospeech.db.models import *
from texttospeech.util import config
from texttospeech.util.antiflood import AntiFlood

antiflood = AntiFlood(max_amount=1, timeout=5)


def create_input_keyboard(user) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(user.get_message('back_button'), callback_data='main_menu')]])


def create_keyboard(user) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(user.get_message('speak_again_button'), callback_data='create_audio')],
         [InlineKeyboardButton(user.get_message('menu_button'), callback_data='main_menu')]]
    )


async def is_flooding(user, message) -> bool:
    if antiflood.is_flooding(user.id):
        if message:
            await message.reply_text(user.get_message('anti_flood'))

        return True

    return False


async def is_above_char_limit(user, message, text) -> bool:
    if len(text) > config.AUDIO_CHARACTER_LIMIT:
        if message:
            await message.reply_text(user.get_message('character_limit_message'))

        return True

    return False


async def send_audio(text: str, client: Client, user: User, chat: Chat = None, keyboard: bool = True,
                     to_delete: Message = None, reply_to_message_id=None, language=None):
    if not language:
        language = user.language

    slow_mode = user.get_setting(Settings.SLOW_MODE, bool)
    file = tts.create_audio(text=text, language=language, slow=slow_mode)

    message = user.get_message('created_with')
    keyboard = create_keyboard(user) if keyboard else None

    if to_delete:
        await to_delete.delete(revoke=True)

    await client.send_voice(chat_id=chat.id if chat else user.id, voice=file, caption=message,
                            reply_markup=keyboard, reply_to_message_id=reply_to_message_id)

    os.remove(file)


async def reply_audio(user, client, message, text, origin, language, chat=None, keyboard=True,
                      reply_to_message_id=None):
    user.reset_action()
    to_delete = await message.reply_text(user.get_message('creating_audio'))

    await send_audio(text=text, client=client, user=user, keyboard=keyboard, to_delete=to_delete,
                     reply_to_message_id=reply_to_message_id, language=language, chat=chat)

    Audio.create(user=user, chat=chat, origin=origin)


async def execute(client, message, origin, chat=None, keyboard=True, reply_to_message_id=None):
    user = message.db_user
    language = user.language
    text = ' '.join(message.command[1:]).strip() if message.command else message.text

    if await is_flooding(user, message) or await is_above_char_limit(user, message, text):
        return

    text = text.replace('\n', '').strip()

    if not text:
        return

    await reply_audio(user=user, client=client, message=message,
                      text=text, origin=origin, language=language,
                      keyboard=keyboard, reply_to_message_id=reply_to_message_id,
                      chat=chat)


@Client.on_message(filters.command(['tts', 'speak', 'audio']) & filters.private)
async def on_speak_command_private(client, message):
    user = message.db_user

    if len(message.command) < 2:
        user.set_action('create_audio')

        msg = user.get_message('awaiting_text')
        keyboard = create_input_keyboard(user)

        await message.reply_text(msg, reply_markup=keyboard)
    else:
        await execute(client=client, message=message, origin=AudioOrigin.COMMAND)


@Client.on_message(cfilters.group_command(['tts', 'speak', 'audio']) & filters.group)
async def on_speak_command_group(client, message):
    user = message.db_user
    chat = message.db_chat

    if len(message.command) < 2:
        await message.reply_text(user.get_message('group_speak_no_arguments'))
    else:
        reply_to_message_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id

        await execute(client=client, message=message, origin=AudioOrigin.GROUP, keyboard=False,
                      chat=chat, reply_to_message_id=reply_to_message_id)


@Client.on_callback_query(cfilters.callback_data('create_audio'))
async def on_speak_callback(_, callback):
    user = callback.db_user
    user.set_action('create_audio')

    msg = user.get_message('awaiting_text')
    keyboard = create_input_keyboard(user)

    await callback.answer()

    if callback.message and callback.message.voice:
        try:
            await callback.edit_message_reply_markup(None)
        except RPCError:  # Message not edited...
            pass

        await callback.message.reply_text(msg, reply_markup=keyboard)
    else:
        await callback.edit_message_text(msg, reply_markup=keyboard)


@Client.on_message(filters.text & cfilters.not_command() & ~filters.via_bot & filters.private &
                   (cfilters.action('create_audio') | cfilters.setting(Settings.ALWAYS_SPEAK)) &
                   ~filters.edited)
async def on_speak_text(client, message):
    keyboard = message.db_user.action == 'create_audio'
    origin = AudioOrigin.BUTTON if keyboard else AudioOrigin.ALWAYS_SPEAK

    await execute(client=client, message=message, origin=origin, keyboard=keyboard)
