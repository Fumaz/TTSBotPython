import os
from datetime import datetime

from pyrogram import Client

from texttospeech.util import config

client = Client(session_name=config.SESSION_NAME,
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                plugins=dict(root=config.PLUGINS_DIR),
                bot_token=config.BOT_TOKEN,
                workers=16)


def clear_audios():
    audios = os.listdir(config.AUDIOS_DIR)
    print(f'Clearing {len(audios)} old audios...')

    for audio in audios:
        try:
            os.remove(config.AUDIOS_DIR + audio)
        except:
            pass


def run():
    clear_audios()

    client.start_time = datetime.now()
    client.run()
