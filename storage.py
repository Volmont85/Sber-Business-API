import redis
from datetime import date

class Storage:

    def __init__(self, redis_url):

        self.redis = redis.from_url(redis_url)

    def get_external_id(self):

        return f"overnight-{date.today()}"

    def acquire_lock(self):

        key = f"overnight-lock:{date.today()}"
        return self.redis.set(key, "1", nx=True, ex=7200)

    def release_lock(self):

        key = f"overnight-lock:{date.today()}"
        self.redis.delete(key)

    def mark_application_created(self):

        key = f"overnight-created:{date.today()}"
        self.redis.set(key, "1", ex=86400)

    def application_created(self):

        key = f"overnight-created:{date.today()}"
        return self.redis.exists(key)

    def mark_completed(self):

        key = f"overnight-complete:{date.today()}"
        self.redis.set(key, "1", ex=86400)

    def already_completed(self):

        key = f"overnight-complete:{date.today()}"
        return self.redis.exists(key)
