# TextToSpeech 🔊
This bot allows you to turn any text into an audio directly on Telegram.<br>
It works in private chats, in groups, and even inline!

It is available on Telegram at https://t.me/TTSBot


### Does the bot save my audios?
The bot only stores audio files temporarily and deletes them immediately after they've been sent to Telegram.
The bot never saves any of your audios or their text in its database, and never will.
The only information that is stored in the DB is for statistics purposes only.

### Self Hosting
If you decide to host the bot yourself, you will need:
- Basic understanding of docker and docker-compose
- Basic understanding of python
- Basic understanding of postgresql
- An API Key and API Hash (https://my.telegram.org)
- A Telegram Bot API Token (https://t.me/BotFather)

Once you have meet all the requirements, you can simply edit the docker-compose.yml file and the config.py file according to your needs, and start up the bot by using `docker compose up -d`.
