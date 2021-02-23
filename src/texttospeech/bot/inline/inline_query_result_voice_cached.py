from typing import Union

from pyrogram import raw
from pyrogram import types
from pyrogram.parser import Parser
from pyrogram.types.inline_mode.inline_query_result import InlineQueryResult
from pyrogram.utils import get_input_media_from_file_id


class InlineQueryResultCachedDocument(InlineQueryResult):
    def __init__(
            self,
            title: str,
            file_id: str,
            file_ref: str = None,
            id: str = None,
            description: str = None,
            caption: str = "",
            parse_mode: Union[str, None] = object,
            reply_markup: "types.InlineKeyboardMarkup" = None,
            input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("file", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.file_ref = file_ref
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self):
        document = get_input_media_from_file_id(self.file_id)

        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            document=document.id,
            send_message=(
                await self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **await(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )
