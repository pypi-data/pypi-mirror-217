from pydantic import validate_arguments
from parsel import Selector

from ...settings import DRAGON_ELEMENTS, SECONDS_PER_DAY

class TowerIslandsParser:
    @validate_arguments
    def __init__(self, html: str) -> None:
        self.__selector = Selector(html)
    
    @property
    def name(self) -> str:
        name = (self.__selector
            .css("h1::text")
            .get()
            .strip()
            .removesuffix(" Tower Island"))

        return name

    @property
    def max_points_per_collection(self) -> int:
        max_points_per_collection = int(self.__selector.css(".tkn_hold div b::text").get())
        return max_points_per_collection

    @property
    def duration(self) -> int:
        duration = int(self.__selector
            .css(".dur_text::text")
            .get()
            .strip()
            .removeprefix("This event lasts ")
            .removesuffix(" days")) * SECONDS_PER_DAY

        return duration

    @property
    def dragons(self) -> list[dict]:
        dragons_selector = self.__selector.css(".over")

        dragons = []

        for dragon_selector in dragons_selector:
            dragon_name = (dragon_selector
                .css(".pan_ic::text")
                .get()
                .strip())

            dragon_rarity = (dragon_selector
                .css(".img_rar::attr(class)")
                .get()
                .split()[0]
                .removeprefix("img_rp_")
                .upper())
            
            dragon_elements = [
                DRAGON_ELEMENTS[element_selector
                    .css("::attr(class)")
                    .get()
                    .split()[1]
                    .removeprefix("tb_")] for element_selector in dragon_selector.css(".typ_i")
            ]

            dragon_image_url = (dragon_selector
                .css(".pan_img::attr(src)")
                .get()
                .replace(" ", "%20")
                .replace("../../", "https://deetlist.com/dragoncity/"))

            dragon_page_url = (dragon_selector.css(".aitm a::attr(href)")
                .get()
                .replace(" ", "%20")
                .replace("../../", "https://deetlist.com/dragoncity/"))

            dragons.append(dict(
                name = dragon_name,
                rarity = dragon_rarity,
                elements = dragon_elements,
                image_url = dragon_image_url,
                page_url = dragon_page_url
            ))

        return dragons

    def get(self) -> dict:
        return dict(
            name = self.name,
            max_points_per_collection = self.max_points_per_collection,
            duration = self.duration,
            dragons = self.dragons
        )

__all__ = [ "TowerIslandsParser" ]