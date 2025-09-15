import redis
from .storage_strategy import StorageStrategy
from datetime import datetime
import getpass
from src.constants import *


class RedisStorage(StorageStrategy):
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def save(self, level, score):
        name = getpass.getuser()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        key = f"scores:{level}"

        self.r.zadd(key, {name: score})

        self.r.hset(f"user:{name}:meta", mapping={
            "last_play": now,
            "last_level": level,
            "last_score": score
        })

    def load(self, level):
        key = f"scores:{level}"

        best = self.r.zrevrange(key, 0, 0, withscores=True)

        if best:
            return int(best[0][1])
        else:
            return 0
