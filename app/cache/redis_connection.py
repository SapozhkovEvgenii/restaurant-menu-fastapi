import redis.asyncio as r  # type: ignore

redis = r.from_url(
    'redis://redis:6379',
    encoding='utf-8',
    decode_responses=True,
)
