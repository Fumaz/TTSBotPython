from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardButton

from texttospeech.bot import cfilters
from texttospeech.localization import languages


@Client.on_message(filters.command('language') & filters.private)
async def on_language_command(_, message):
    user = message.db_user
    user.reset_action()

    back = InlineKeyboardButton(user.get_message('back_button'), callback_data='main_menu')
    await message.reply_text(user.get_message('language_selection'), reply_markup=languages.create_keyboard(back))


@Client.on_callback_query(cfilters.callback_data('change_language'))
async def on_language_callback(_, callback):
    user = callback.db_user
    back = InlineKeyboardButton(user.get_message('back_button'), callback_data='settings')

    await callback.answer()
    await callback.edit_message_text(user.get_message('language_selection'),
                                     reply_markup=languages.create_keyboard(back))


@Client.on_callback_query(filters.regex('^set_language_'))
async def on_set_language_callback(_, callback):
    callback.db_user.set_language(callback.data[len('set_language_'):])

    try:
        await callback.answer(callback.db_user.get_message('language_set'), show_alert=True)
        await callback.edit_message_text(callback.db_user.get_message('language_selection'),
                                         reply_markup=callback.message.reply_markup)
    except RPCError:  # If the language was the same (message wasn't edited)
        pass
