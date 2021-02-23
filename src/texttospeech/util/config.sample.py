API_ID = -1  # Insert your API ID
API_HASH = ""  # Insert your API Hash

BOT_TOKEN = ""  # Insert your bot token
BOT_USERNAME = ""  # Insert your bot's username
BOT_WORKERS = 8  # Insert the workers amount

SESSION_NAME = "session"

DB_CON = {
    'provider': 'postgres',
    'host': 'postgres',
    'user': 'postgres',
    'password': '',
    'database': 'tts'
}

LANGUAGES_DIR = "languages/"  # Your languages directory
PLUGINS_DIR = 'texttospeech/bot/plugin'
AUDIOS_DIR = 'audios/'  # Your audios directory

AUDIOS_DOMAIN = 'https://audio.example.org'  # Domain for audios (inline)
AUDIO_THUMB_URL = 'https://i.imgur.com/Ginyq2C.png'  # Thumbnail for inline audios
ERROR_THUMB_URL = 'https://i.imgur.com/RARF2nv.png'  # Thumbnail for inline errors
AUDIO_CHARACTER_LIMIT = 500  # The character limit for an audio
