from texttospeech.audio import tts
from texttospeech.bot import bot
from texttospeech.db import models
from texttospeech.web import web

if __name__ == '__main__':
    models.setup()
    tts.setup()
    web.run()
    bot.run()
