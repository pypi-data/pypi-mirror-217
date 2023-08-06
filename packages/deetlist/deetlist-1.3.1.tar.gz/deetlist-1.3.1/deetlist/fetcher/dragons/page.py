from pydantic import validate_arguments
import httpx

from ..base import BaseFetcher, BaseAsyncFetcher

@validate_arguments
async def fetch_async_dragon_page(url_or_dragon_name: str):
    if not url_or_dragon_name.startswith("http://") and not url_or_dragon_name.startswith("https://"):
        dragon_name_parsed = url_or_dragon_name.title().replace(" ", "%20")
        url = f"https://deetlist.com/dragoncity/dragon/{dragon_name_parsed}"

    else:
        url = url_or_dragon_name

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url)
        return response.text

class DragonPageFetcher(BaseFetcher):
    @validate_arguments
    def __init__(self, url_or_dragon_name: str) -> None:
        if not url_or_dragon_name.startswith("http://") and not url_or_dragon_name.startswith("https://"):
            dragon_name_parsed = url_or_dragon_name.title().replace(" ", "%20")
            url = f"https://deetlist.com/dragoncity/dragon/{dragon_name_parsed}"

        else:
            url = url_or_dragon_name

        super().__init__(url)

class DragonPagesAsyncFetcher(BaseAsyncFetcher):
    __urls_params = []

    @validate_arguments
    def __init__(self, urls: list[str]) -> None:
        for url in urls:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = f"https://deetlist.com/dragoncity/dragon/{url.title().replace(' ', '%20')}"

            self.__urls_params.append((url, None))

    @validate_arguments
    def run(self) -> list[dict]:
        return super().run(self.__urls_params)

__all__ = [ "DragonPageFetcher", "DragonPagesAsyncFetcher" ]