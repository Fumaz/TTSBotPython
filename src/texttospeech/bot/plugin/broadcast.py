import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.methods.messages.send_chat_action import ChatAction
from pyrogram.types import Message

from texttospeech.bot import cfilters
from texttospeech.db.models import *


@Client.on_message(filters.command("activitycheck") & cfilters.admin)
async def on_activity_check(client: Client, message: Message):
    with db_session:
        total = User.select().count()

    status = await message.reply_text('Checking... 0% (0/{})'.format(total))
    sent = 0
    success = 0
    fail = 0

    inactive = []

    with db_session:
        print('Opened DB Session', flush=True)

        for user_id in select(u.id for u in User if u.is_active):
            try:
                sent += 1

                await client.send_chat_action(user_id, 'typing')
                await asyncio.sleep(0.03)
                success += 1

                if sent % 100 == 0:
                    await status.edit_text('Checking... {}% ({}/{}) ({}/{})'.format(int(sent / total * 100), sent, total, success, fail))
            except FloodWait as e:
                fail += 1
                print('FloodWait: {}'.format(e), flush=True)
                await asyncio.sleep(e.x)
            except Exception as e:
                fail += 1
                await asyncio.sleep(0.03)

                inactive.append(user_id)

                if len(inactive) >= 100:
                    print('dbing inactive users', flush=True)

                    with db_session:
                        for user in inactive:
                            User.get(id=user).is_active = False

                        commit()

                    inactive = []

                if sent % 100 == 0:
                    await status.edit_text('Checking... {}% ({}/{}) ({}/{})'.format(int(sent / total * 100), sent, total, success, fail))


@Client.on_message(filters.command("broadcast") & cfilters.admin & filters.reply)
async def on_broadcast(client: Client, message: Message):
    with db_session:
        total = User.select().count()

    starting = int(message.command[0]) if len(message.command) > 0 else 0

    broadcast = message.reply_to_message
    status = await message.reply_text('Broadcasting... 0% (0/{})'.format(total))
    sent = 0
    success = 0
    fail = 0

    with db_session:
        print('Opened DB Session', flush=True)
        for user_id in select(u.id for u in User if u.is_active):
            try:
                sent += 1

                if sent < starting:
                    continue
                # print('Sending to {} ({}/{}) ({}/{})'.format(user_id, sent, total, success, fail))
                await broadcast.forward(user_id)
                await asyncio.sleep(0.05)
                success += 1

                if sent % 100 == 0:
                    await status.edit_text('Broadcasting... {}% ({}/{}) ({}/{})'.format(int(sent / total * 100), sent, total, success, fail))
            except FloodWait as e:
                fail += 1
                print('FloodWait: {}'.format(e), flush=True)
                await asyncio.sleep(e.x)
            except Exception as e:
                fail += 1
                # print(e, flush=True)
                # await asyncio.sleep(0.05)

                if sent % 100 == 0:
                    await status.edit_text('Broadcasting... {}% ({}/{}) ({}/{})'.format(int(sent / total * 100), sent, total, success, fail))
