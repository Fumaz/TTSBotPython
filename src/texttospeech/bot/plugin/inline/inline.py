import asyncio
import logging

from pyrogram import Client
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

from texttospeech.audio import tts
from texttospeech.bot.inline.inline_query_result_voice import InlineQueryResultVoice
from texttospeech.db.models import AudioOrigin, Settings, Audio
from texttospeech.util import config

latest = {}


def create_keyboard(user) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(user.get_message('inline_create_audio'), switch_inline_query='')]
    ])


def create_error_result(user, message: str) -> InlineQueryResultArticle:
    msg = user.get_message(message)
    keyboard = create_keyboard(user)

    return InlineQueryResultArticle(title=msg, reply_markup=keyboard,
                                    thumb_url=config.ERROR_THUMB_URL,
                                    input_message_content=InputTextMessageContent(message_text=msg))


def create_audio_result(text: str, user, keyboard: bool = True, language=None):
    if not language:
        language = user.language

    link = tts.create_link(text=text, language=language, slow=user.get_setting(Settings.SLOW_MODE, bool))
    title = user.get_message('inline_create_audio')
    caption = user.get_message('created_with')
    keyboard = create_keyboard(user) if keyboard else None

    return InlineQueryResultVoice(voice_url=link,
                                  title=title,
                                  caption=caption,
                                  reply_markup=keyboard)


@Client.on_inline_query()
async def on_inline_query(_, query):
    latest[query.from_user.id] = query.id

    user = query.db_user
    text = query.query.replace('\n', '').strip()

    switch_pm_text = user.get_message('inline_language')
    switch_pm_parameter = 'language'
    results = []

    if not text:
        results.append(create_error_result(user, 'empty_text'))
    else:
        language = user.language

        if len(text.split(' ')[0]) == 2 and tts.is_valid(text[:2]):
            language = text[:2]
            text = text[2:]

        if len(text) > config.AUDIO_CHARACTER_LIMIT:
            results.append(create_error_result(user, 'character_limit_inline'))
        else:
            try:
                await asyncio.sleep(1)  # So that the user doesn't spam inline requests because TG is dumb

                if latest[query.from_user.id] != query.id:
                    return

                result = create_audio_result(text, user, language=language)

                if result:
                    results.append(result)
            except Exception as e:
                results.append(create_error_result(user, 'empty_text'))
                logging.error('An error occured whilst creating an inline audio.', exc_info=e)

    await query.answer(results=results, cache_time=0, is_personal=True,
                       switch_pm_text=switch_pm_text, switch_pm_parameter=switch_pm_parameter)


@Client.on_chosen_inline_result()
async def on_chosen_inline_result(_, chosen):
    Audio.create(chosen.db_user, origin=AudioOrigin.INLINE)
