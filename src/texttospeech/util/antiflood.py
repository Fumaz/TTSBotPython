from datetime import datetime, timedelta


class AntiFlood:
    def __init__(self, max_amount: int, timeout: int):
        self.cache = {}
        self.max_amount = max_amount
        self.timeout = timeout

    def is_flooding(self, key) -> bool:
        if key not in self.cache:
            self.cache[key] = user_cache = []
        else:
            user_cache = self.cache[key]

        for dt in user_cache:
            if dt < datetime.now() - timedelta(seconds=self.timeout):
                user_cache.remove(dt)

        user_cache.append(datetime.now())

        return len(user_cache) > self.max_amount
