from loguru import logger
import asyncio, random

from settings import RETRY_COUNT


async def sleep(sleep_from: int, sleep_to: int) -> None:
    delay = random.randint(sleep_from, sleep_to)
    logger.info(f'Спим {delay} секунд...')
    for _ in range(delay):
        await asyncio.sleep(1)

def retry(func) -> callable:
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries < RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                if 'insufficient' in str(e):
                    logger.error('Недостаточно средств!')
                else:
                    logger.error(e)
                await sleep(20, 30)
                retries += 1
    return wrapper
