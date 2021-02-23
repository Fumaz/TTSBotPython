import logging
from typing import Optional

from plate import Plate
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..util import config


plate = Plate(root=config.LANGUAGES_DIR)


def match_closest(language: str) -> str:
    """
    Gets the closest language that matches the given string.

    :param language: the language to match
    :return: the language that was found
    """

    if not language:
        return 'en_US'

    for locale in plate.locales.keys():
        if locale[:2] == language[:2]:
            return locale

    return 'en_US'


def get_message(message_name: str, language_name: str = 'en_US', **kwargs) -> Optional[str]:
    """
    Gets a localized message. If the message does not exist in the selected language, it will use English.

    :param message_name: the message
    :param language_name: the language
    :param kwargs: additional arguments passed to the message
    :return: the localized message
    """

    language_name = match_closest(language_name)

    if 'user' in kwargs:
        kwargs['first_name'] = kwargs['user'].first_name
        kwargs['full_name'] = kwargs['user'].full_name
        kwargs['mention'] = kwargs['user'].mention

    try:
        kwargs['flag'] = plate('flag', language_name)
        return plate(message_name, language_name, **kwargs)
    except ValueError as e:
        logging.error(f'An error occured whilst fetching {message_name} in language {language_name}', exc_info=e)

        if language_name == 'en_US':
            return None

        kwargs['flag'] = plate('flag', 'en_US')
        return plate(message_name, 'en_US', **kwargs)


def create_keyboard(back: InlineKeyboardButton = None) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard for language selection.

    :param back: The back button on the keyboard (to go back to the previous menu)
    :return: the keyboard
    """

    keyboard = [[]]

    for lang in plate.locales:
        if len(keyboard[-1]) >= 3:
            keyboard.append([])

        flag = plate('flag', lang)
        keyboard[-1].append(InlineKeyboardButton(flag, callback_data=f'set_language_{lang}'))

    if back:
        keyboard.append([back])

    return InlineKeyboardMarkup(keyboard)


def create_message_data(user) -> dict:
    """
    Creates the language selection message data.

    :param user: the user
    :return: a dict containing text and reply_markup
    """

    msg = user.get_message('language_selection')
    back = InlineKeyboardButton(user.get_message('back_button'), callback_data='settings')
    keyboard = create_keyboard(back=back)

    return dict(text=msg, reply_markup=keyboard)
