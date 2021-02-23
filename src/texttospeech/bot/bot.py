from datetime import datetime

from pyrogram import Client

from texttospeech.util import config

client = Client(session_name=config.SESSION_NAME,
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                plugins=dict(root=config.PLUGINS_DIR),
                bot_token=config.BOT_TOKEN,
                workers=config.BOT_WORKERS)


def run():
    client.start_time = datetime.now()
    client.run()
