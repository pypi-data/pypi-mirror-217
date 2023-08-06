from pydantic import validate_arguments
import asyncio
import random

from ..scraper.dragons import scrape_all_dragons, scrape_async_dragon_page

FloatOrInt = float | int

@validate_arguments
async def crawl_dragons(
    urls_or_dragon_names: list[str],
    attempt_limit: int = 5,
    interval_between_attempts: tuple[FloatOrInt, FloatOrInt] = (3, 6),
):
    @validate_arguments
    async def _scrape(url_or_dragon_name: str, attempts: int):
        try:
            dragon = await scrape_async_dragon_page(url_or_dragon_name)
            return dragon

        except:
            if attempts >= attempt_limit: return

            rand_time_to_sleep = random.randint(*interval_between_attempts)

            await asyncio.sleep(rand_time_to_sleep)
            return await _scrape(attempts + 1)

    tasks = [
        _scrape(url_or_dragon_name, 0)
        for url_or_dragon_name in urls_or_dragon_names
    ]

    dragons = await asyncio.gather(*tasks)
    dragons = list(
        filter(lambda dragon: dragon != None, dragons)
    )

    return dragons

def crawl_all_dragons():
    all_dragons_urls = [ dragon["page_url"] for dragon in scrape_all_dragons() ]
    all_dragons = asyncio.run(crawl_dragons(all_dragons_urls))
    return all_dragons

