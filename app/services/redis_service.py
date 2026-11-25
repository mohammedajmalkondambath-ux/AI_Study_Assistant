
import redis


class RedisService:
    """Manages Redis cache connections."""

    def __init__(self, host: str = "localhost", port: int = 6379):
        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

    def test_connection(self) -> bool:
        """Check whether Redis is responding."""

        result = self.client.ping()

        print("Redis connected successfully.")

        return result

    def set_value(self, key: str, value: str, expiry: int = 3600):
        """Store a value in Redis with an expiry time."""

        self.client.setex(key, expiry, value)

    def get_value(self, key: str):
        """Retrieve a cached value."""

        return self.client.get(key)

    def close(self) -> None:
        """Close the Redis connection."""

        self.client.close()
