import random
import string

CHARACTERS = string.ascii_letters + string.digits


def random_name(length: int = 16, extension: str = '') -> str:
    return ''.join(random.choices(CHARACTERS, k=length)) + ('.' + extension if extension else '')