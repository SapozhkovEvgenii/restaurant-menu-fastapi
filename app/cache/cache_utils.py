import json

from fastapi.encoders import jsonable_encoder

from app.cache.redis_connection import redis


async def get_cache(prefix, body):
    key = generate_key(prefix, body)
    value = await redis.get(key)
    return json.loads(value) if value else None


async def set_cache(prefix, body, value):
    key = generate_key(prefix, body)
    await redis.set(key, json.dumps(jsonable_encoder(value)))


async def clear_cache(prefix, body):
    key = generate_key(prefix, body)
    keys = await redis.keys(f'{key}*')
    if keys:
        await redis.delete(*keys)


def generate_key(prefix, body):
    key = f'{prefix}:{body}'
    return key
