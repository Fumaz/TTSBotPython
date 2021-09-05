import logging
import os
from threading import Thread
from time import sleep

import ffmpeg
from gtts import gTTS
from gtts.lang import tts_langs

from texttospeech.util import config, files

langs = None


def setup():
    """
    Fetches the available languages from google's TTS API.
    """
    global langs

    try:
        langs = tts_langs()
    except RuntimeError as e:
        logging.error('An error occured whilst fetching the langs.', exc_info=e)
        exit(0)


def is_valid(language: str) -> bool:
    """
    Checks if a language is valid

    :param language: the language to check
    :return: true if the language is valid, false otherwise
    """

    return language in langs


def create_mp3(text: str, language: str = 'en_US', slow: bool = False) -> str:
    """
    Creates an mp3 file.

    :param text: the text of the audio
    :param language: the language of the audio
    :param slow: if the audio should be slowed down
    :return: the created file's path
    """

    filename = os.path.join(config.AUDIOS_DIR, files.random_name(extension='mp3'))
    gtts = gTTS(text=text, lang=language[:2], slow=slow, lang_check=False)

    try:
        gtts.save(filename)

        return filename
    except RuntimeError as e:
        logging.error('An error occured whilst saving the audio.', exc_info=e)


def convert_to_ogg(filename: str) -> str:
    """
    Converts a file to .ogg

    :param filename: the file to convert
    :return: the created file's path
    """

    output = filename[:-3] + 'ogg'

    try:
        stream = ffmpeg.input(filename).output(output, ar='48000', ac=2, acodec='libopus', ab='32k', threads=2)
        ffmpeg.run(stream, quiet=True)

        return output
    except RuntimeError as e:
        logging.error('An error occured whilst converting the file.', exc_info=e)


def create_audio(text: str, language: str = 'en_US', slow: bool = False) -> str:
    """
    Creates an audio file with .ogg extension

    :param text: the text of the audio
    :param language: the language of the audio
    :param slow: if the audio should be slowed down
    :return: the created file's path
    """

    in_file = create_mp3(text=text, language=language, slow=slow)
    out_file = convert_to_ogg(in_file)

    os.remove(in_file)

    return out_file


def create_link(text: str, language: str = 'en_US', slow: bool = False) -> str:
    """
    Creates an audio file and returns its link

    :param text: the text of the audio
    :param language: the language of the audio
    :param slow: if the audio should be slowed down
    :return: the url of the created file
    """

    filename = create_audio(text=text, language=language, slow=slow)

    def remove_audio():
        sleep(45)
        os.remove(filename)

    Thread(target=remove_audio).start()

    return f'{config.AUDIOS_DOMAIN}/{filename.split("/")[-1]}'
