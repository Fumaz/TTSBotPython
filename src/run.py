import sentry_sdk

from texttospeech.audio import tts
from texttospeech.bot import bot
from texttospeech.db import models
from texttospeech.web import web
from texttospeech.util import config

if __name__ == '__main__':
    sentry_sdk.init(
        config.SENTRY_URL,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

    try:
        1/0
    except Exception as e:
        sentry_sdk.capture_exception(e)

    models.setup()
    tts.setup()
    web.run()
    bot.run()
