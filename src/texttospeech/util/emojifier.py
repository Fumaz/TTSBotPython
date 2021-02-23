class Emoji:
    @staticmethod
    def from_boolean(value: bool) -> str:
        return '✅' if value else '❌'
