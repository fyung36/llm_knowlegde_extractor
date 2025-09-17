from redis.asyncio import Redis

from src.config import settings

JTI_EXPIRE = 30 * 24 * 60 * 60

redis_pool = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=0,
    ssl=settings.REDIS_SSL,
    decode_responses=True,  # This ensures we get strings back, not bytes
)


async def add_jti_to_blocklist(jti: str) -> None:
    await redis_pool.set(name=jti, value="", ex=JTI_EXPIRE)


async def token_in_blocklist(jti: str) -> bool:
    jti = await redis_pool.get(jti)

    return jti is not None


async def close_redis_connection():
    await redis_pool.close()
