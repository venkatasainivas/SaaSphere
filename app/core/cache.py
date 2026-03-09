import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Connect to Redis
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def set_cache(key: str, value: dict, expire: int = 300):
    """Save data to Redis cache"""
    try:
        redis_client.setex(key, expire, json.dumps(value))
    except Exception as e:
        print(f"Cache set error: {e}")

def get_cache(key: str):
    """Get data from Redis cache"""
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None

def delete_cache(key: str):
    """Delete data from Redis cache"""
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Cache delete error: {e}")

def clear_tenant_cache(tenant_id: int):
    """Clear all cache for a tenant"""
    try:
        keys = redis_client.keys(f"tenant:{tenant_id}:*")
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print(f"Cache clear error: {e}")