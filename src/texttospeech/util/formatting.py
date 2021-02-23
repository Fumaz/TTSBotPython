from texttospeech.util import config

DEEP_LINKING = f'https://t.me/{config.BOT_USERNAME}?start='
DEEP_GROUPING = f'https://t.me/{config.BOT_USERNAME}?startgroup='
INVISIBLE_CHAR = '⠀'

HTML_LINK = "<a href='{url}'>{text}</a>"


def link(url: str, text: str) -> str:
    return HTML_LINK.format(url=url, text=text)


def invisible_link(url: str) -> str:
    return link(url=url, text=INVISIBLE_CHAR)


def deeplink(path: str) -> str:
    return DEEP_LINKING + path


def deepgroup(path: str) -> str:
    return DEEP_GROUPING + path
