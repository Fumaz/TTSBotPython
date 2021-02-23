from typing import Union

from pyrogram import filters

from texttospeech.util import config

admin = filters.create(lambda _, __, update: update.db_user.is_admin)
banned = filters.create(lambda _, __, update: update.db_user.is_banned)
added = filters.create(lambda _, __, update: getattr(update, 'self_was_added', False))


def callback_data(data: str):
    async def func(_, __, callback):
        return callback.data == data

    return filters.create(func, "CallbackDataFilter")


def action(action: str):
    async def func(_, __, update):
        return update.db_user and update.db_user.action == action

    return filters.create(func, "ActionFilter")


def not_command(prefixes=None):
    if not prefixes:
        prefixes = ['/']

    async def func(_, __, message):
        for prefix in prefixes:
            if message.text.startswith(prefix):
                return False

        return True

    return filters.create(func, "NotCommandFilter")


def setting(name: str):
    async def func(_, __, update):
        return bool(update.db_user) and bool(update.db_user.get_setting(name, bool))

    return filters.create(func, "SettingFilter")


def group_setting(name: str):
    async def func(_, __, update):
        return bool(update.db_chat) and bool(update.db_chat.get_setting(name, bool))

    return filters.create(func, "SettingFilter")


def group_command(commands: Union[str, list], prefixes: Union[str, list] = "/"):
    if not isinstance(commands, list):
        commands = [commands]

    for command in list(commands):
        commands.append(f'{command}@{config.BOT_USERNAME}')

    return filters.command(commands, prefixes)
