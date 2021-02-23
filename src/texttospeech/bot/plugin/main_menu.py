from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from texttospeech.bot import cfilters
from texttospeech.bot.plugin import settings, language
from texttospeech.util import formatting


def create_keyboard(user) -> InlineKeyboardMarkup:
    speak = InlineKeyboardButton(user.get_message('speak_button'),
                                 callback_data="create_audio")

    about_me = InlineKeyboardButton(user.get_message('info_button'),
                                    callback_data='info')

    stats = InlineKeyboardButton(user.get_message('stats_button'),
                                 callback_data='stats')

    settings = InlineKeyboardButton(user.get_message('settings_button'),
                                    callback_data='settings')

    inline = InlineKeyboardButton(user.get_message('inline_button'),
                                  switch_inline_query='')

    group = InlineKeyboardButton(user.get_message('add_to_group_button'),
                                 url=formatting.deepgroup('added'))

    return InlineKeyboardMarkup([[speak], [settings, inline], [about_me, stats], [group]])


def create_message(user) -> str:
    return user.get_message('main_menu', image='')


@Client.on_message(filters.command('start') & filters.private)
async def on_start_command(client, message):
    user = message.db_user
    user.reset_action()

    if len(message.command) > 1:
        arg = message.command[1].lower()

        if arg == 'language':
            await language.on_language_command(client, message)
            return
        elif arg == 'settings':
            await settings.on_settings_command(client, message)
            return

    await message.reply_text(create_message(user), reply_markup=create_keyboard(user), disable_web_page_preview=False)


@Client.on_callback_query(cfilters.callback_data('main_menu'))
async def on_start_callback(_, callback):
    user = callback.db_user
    user.reset_action()

    await callback.answer()

    if callback.message.voice:
        try:
            await callback.edit_message_reply_markup(None)
        except RPCError:  # Message already has empty keyboard or is deleted
            pass

        await callback.message.reply_text(create_message(user), reply_markup=create_keyboard(user),
                                          disable_web_page_preview=False)
    else:
        await callback.edit_message_text(create_message(user), reply_markup=create_keyboard(user),
                                         disable_web_page_preview=False)
