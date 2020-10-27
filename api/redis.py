import redis
import sys
from api.settings import REDIS_HOST, REDIS_PORT


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)
