from typing import Union

from pyrogram.parser import Parser
from pyrogram.raw import types
from pyrogram.types import InlineQueryResult, InlineKeyboardMarkup, InputMessageContent


class InlineQueryResultVoice(InlineQueryResult):
    def __init__(
            self,
            voice_url: str,
            title: str,
            thumb_url: str = None,
            id: str = None,
            description: str = None,
            caption: str = None,
            parse_mode: Union[str, None] = object,
            reply_markup: InlineKeyboardMarkup = None,
            input_message_content: InputMessageContent = None
    ):
        super().__init__("voice", id, input_message_content, reply_markup)

        self.voice_url = voice_url
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    """Link to a voice file.

    By default, this voice file will be sent by the user with optional caption.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    voice.

    Parameters:
        voice_url (``str``):
            A valid URL for the voice file.
            File size must not exceed 1 MB.

        thumb_url (``str``, *optional*):
            URL of the static thumbnail for the result (jpeg or gif)
            Defaults to the value passed in *voice_url*.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        title (``str``, *optional*):
            Title for the result.

        description (``str``, *optional*):
            Short description of the result.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.

        input_message_content (:obj:`InputMessageContent`):
            Content of the message to be sent instead of the voice file.
    """

    async def write(self, client: "pyrogram.Client"):
        voice = types.InputWebDocument(
            url=self.voice_url,
            size=0,
            mime_type="audio/ogg",
            attributes=[]
        )

        if self.thumb_url is None:
            thumb = None
        else:
            thumb = types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            )

        return types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=voice,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    **await(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )
