import redis
from datetime import datetime


class Storage:

    def __init__(self, redis_url):

        self.redis = redis.from_url(redis_url)

    def lock_today(self):

        key = "overnight:" + datetime.now().strftime("%Y-%m-%d")

        return self.redis.setnx(key, "1")
