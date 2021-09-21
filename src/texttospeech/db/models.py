import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union, Type

from pony.orm import *
# Still no enum support in pony :(
from pyrogram import types

from texttospeech.localization import languages
from texttospeech.util import config
from texttospeech.util.emojifier import Emoji

db = Database()
updates = Union[types.User, types.Message, types.InlineQuery,
                types.ChosenInlineResult, types.CallbackQuery]


class Settings:
    """
    Available bot settings.
    """

    WELCOME_SENT = 'welcome_sent'
    ALWAYS_SPEAK = 'always_speak'
    SLOW_MODE = 'slow_mode'
    LANGUAGE = 'language'
    ACTION = 'action'
    BANNED = 'banned'
    ADMIN = 'admin'


class ChatType:
    """
    Possible chat types.
    """

    GROUP = 'group'
    CHANNEL = 'channel'
    SUPERGROUP = 'supergroup'

    @staticmethod
    def from_chat(chat: types.Chat) -> str:
        return getattr(ChatType, chat.type.upper(), None)


class AudioOrigin:
    """
    How was an audio generated?
    """

    UNKNOWN = 'unknown'
    ALWAYS_SPEAK = 'always_speak'
    INLINE = 'inline'
    BUTTON = 'button'
    COMMAND = 'command'
    GROUP = 'group'


class StartReason:
    """
    How did a user find the bot?
    """

    UNKNOWN = 'unknown'
    MESSAGE = 'message'
    INLINE = 'inline'
    CALLBACK = 'callback'
    GROUP = 'group'

    @staticmethod
    def from_update(update: updates) -> str:
        if isinstance(update, types.Message):
            if update.chat.type != 'private' and update.chat.type != 'bot':
                return StartReason.GROUP

            return StartReason.MESSAGE

        if isinstance(update, types.InlineQuery) or isinstance(update, types.ChosenInlineResult):
            return StartReason.INLINE

        if isinstance(update, types.CallbackQuery):
            return StartReason.CALLBACK

        return StartReason.UNKNOWN

# noinspection PyArgumentList
class User(db.Entity):
    """
    A telegram user.
    """

    id = PrimaryKey(int, size=64)
    first_name = Required(str)
    last_name = Optional(str)
    username = Optional(str)
    is_bot = Required(bool, default=False)
    dc_id = Optional(int)
    start_reason = Required(str, default=StartReason.UNKNOWN)
    last_update = Required(datetime, default=datetime.now)
    creation_date = Required(datetime, default=datetime.now)

    audios = Set('Audio')
    settings = Set('Setting')

    @staticmethod
    @db_session
    def from_pyrogram(tg_user: updates) -> Union['User', None]:
        start_reason = StartReason.from_update(tg_user)

        if not isinstance(tg_user, types.User):
            tg_user = tg_user.from_user

        if not tg_user:
            return None

        user_id = tg_user.id
        first_name = tg_user.first_name
        last_name = tg_user.last_name or ''
        username = tg_user.username or ''
        is_bot = tg_user.is_bot
        language = languages.match_closest(tg_user.language_code)
        dc_id = tg_user.dc_id

        if not (db_user := User.get(id=user_id)):
            db_user = User(id=user_id,
                           first_name=first_name,
                           last_name=last_name,
                           username=username,
                           dc_id=dc_id,
                           is_bot=is_bot,
                           start_reason=start_reason)

            Setting(user=db_user, name=Settings.LANGUAGE, value=language)
        else:
            db_user.first_name = first_name
            db_user.last_name = last_name
            db_user.username = username

        return db_user

    def before_update(self):
        self.last_update = datetime.now()

    def get_message(self, name: str, **kwargs) -> str:
        from ..localization.languages import get_message

        return get_message(message_name=name, language_name=self.language, user=self, **kwargs)

    @db_session
    def get_setting(self, name: str, type: Type = str):
        setting = self.current.settings.select(lambda s: s.name == name)

        value = None

        if len(setting) > 0:
            value = setting.first().value

        if type is bool or type is Emoji:
            value = value and value.lower() in ('true', 't', 'yes')

        if type is Emoji:
            value = Emoji.from_boolean(value)

        return value

    @db_session
    def set_setting(self, name: str, value):
        user = self.current
        setting = user.settings.select(lambda s: s.name == name).first()

        if not setting:
            if not value:
                return value

            Setting(user=user, name=name, value=str(value))
        else:
            if not value:
                setting.delete()
                return value

            setting.value = str(value)

        return value

    def toggle_setting(self, name: str):
        return self.set_setting(name=name, value=not self.get_setting(name, bool))

    def remove_setting(self, name: str):
        self.set_setting(name=name, value=None)

    def set_action(self, action: str):
        self.set_setting(Settings.ACTION, action)

    def set_language(self, language: str):
        self.set_setting(Settings.LANGUAGE, language)

    def ban(self):
        self.set_setting(Settings.BANNED, True)

    def unban(self):
        self.set_setting(Settings.BANNED, False)

    def promote(self):
        self.set_setting(Settings.ADMIN, True)

    def demote(self):
        self.set_setting(Settings.ADMIN, False)

    def reset_action(self):
        self.remove_setting(Settings.ACTION)

    @property
    def current(self) -> 'User':
        return User.get(id=self.id)

    @property
    def language(self) -> str:
        return self.get_setting(Settings.LANGUAGE)

    @property
    def is_banned(self) -> bool:
        return self.get_setting(Settings.BANNED, bool)

    @property
    def is_admin(self) -> bool:
        return self.get_setting(Settings.ADMIN, bool)

    @property
    def action(self) -> str:
        return self.get_setting(Settings.ACTION)

    @property
    def full_name(self) -> str:
        return f'{self.first_name}{" " + self.last_name if self.last_name else ""}'

    @property
    def mention(self) -> str:
        return f"<a href='tg://user?id={self.id}>{self.first_name}</a>"


# noinspection PyArgumentList
class Chat(db.Entity):
    """
    A telegram chat.
    """

    id = PrimaryKey(int, size=64)
    title = Required(str)
    username = Optional(str)
    description = Optional(str)
    members_count = Required(int)
    type = Required(str)
    last_update = Required(datetime, default=datetime.now)
    creation_date = Required(datetime, default=datetime.now)

    settings = Set('Setting')
    audios = Set('Audio')

    @staticmethod
    @db_session
    def from_pyrogram(tg_chat: Union[types.Chat, types.Message]) -> Union['Chat', None]:
        if not isinstance(tg_chat, types.Chat):
            tg_chat = tg_chat.chat

        if not tg_chat:
            return None

        if not (chat_type := ChatType.from_chat(tg_chat)):
            return None

        chat_id = tg_chat.id
        title = tg_chat.title
        username = tg_chat.username or ''
        description = tg_chat.description or ''
        members_count = tg_chat.members_count or 0

        if not (db_chat := Chat.get(id=chat_id)):
            db_chat = Chat(id=chat_id, title=title, username=username,
                           description=description, members_count=members_count,
                           type=chat_type)
        else:
            db_chat.title = title
            db_chat.username = username
            db_chat.description = description
            db_chat.members_count = members_count

        return db_chat

    @db_session
    def get_setting(self, name: str, type: Type = str):
        setting = self.current.settings.select(lambda s: s.name == name)

        value = None

        if len(setting) > 0:
            value = setting.first().value

        if type is bool or type is Emoji:
            value = value and value.lower() in ('true', 't', 'yes')

        if type is Emoji:
            value = Emoji.from_boolean(value)

        return value

    @db_session
    def set_setting(self, name: str, value):
        chat = self.current
        setting = chat.settings.select(lambda s: s.name == name).first()

        if not setting:
            if not value:
                return value

            Setting(chat=chat, name=name, value=str(value))
        else:
            if not value:
                setting.delete()
                return value

            setting.value = str(value)

        return value

    def toggle_setting(self, name: str):
        return self.set_setting(name=name, value=not self.get_setting(name, bool))

    def before_update(self):
        self.last_update = datetime.now()

    @property
    def current(self):
        return Chat.get(id=self.id)


class Setting(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Optional(User)
    chat = Optional(Chat)
    name = Required(str)
    value = Required(str)


class Audio(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    chat = Optional(Chat)
    language = Required(str)
    origin = Required(str, default=StartReason.UNKNOWN)
    creation_date = Required(datetime, default=datetime.now)

    @staticmethod
    @db_session
    def create(user: User, chat: Chat = None, origin: str = None, language: str = None) -> 'Audio':
        user = user.current
        chat = chat.current if chat else None

        if not language:
            language = user.language

        return Audio(user=user, chat=chat, language=language, origin=origin)


def setup():
    db.bind(config.DB_CON)
    db.generate_mapping(create_tables=True)

    logging.warning('Database connected successfully.')
