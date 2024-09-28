import sys

import nodriver as uc
from bs4 import BeautifulSoup

from . import parsers
from .utils import extract_url_param
from .interfaces import Interface
from .schemas import CAR_EXTRACTION_PLAN
# import parsers
# from interfaces import CarInterface, MotorcycleInterface


class AvtonetScraper:
    def __init__(self) -> None:
        pass

    async def _get_html_async(self, url):
        # Navigate to url and get html content
        browser = await uc.start(
            headless=True,
        )

        page = await browser.get(url)
        html = await page.get_content()
        await page.close()

        return BeautifulSoup(html, "lxml")

    def get_html(self, url: str) -> BeautifulSoup:
        return uc.loop().run_until_complete(self._get_html_async(url))

    def determine_vehicle_type(self, soup: BeautifulSoup):
        element = soup.find("i", {"class": "flaticon-029-time"})
        return "car" if element else "motorcycle"

    def check_vehicle_availabilitiy(self, soup):
        container = soup.find("div", {"class": "col-12 h3 mt-5 mb-5 text-center"})
        if not container:
            return True, ""

        texts = list(container.stripped_strings)
        if "ni več aktualna" in texts[0]:
            text = " ".join(texts)
            text = text.replace("\n", "")
            return False, text
        return True, ""

    def get_vehicle(self, url: str=None, id: int=None):
        if not url and not id:
            return {
                "error": "Specify identifier"
            }
        if not url:
            url = f"https://www.avto.net/Ads/details.asp?id={id}"

        # Get html, make the soup
        soup = self.get_html(url)

        # Check if vehicle is still available
        is_available, status = self.check_vehicle_availabilitiy(soup)

        if not is_available:
            return {
                "error": "Vehicle is no longer available",
            }

        # Determine vehicle type (car/motorcycle)
        vehicle_type = self.determine_vehicle_type(soup)

        data = {}

        if vehicle_type == "car":
            interface = Interface(soup)
            data = interface.get_data(CAR_EXTRACTION_PLAN)
            if data.get("error"):
                return data

            data["vehicleType"] = "car"
        elif vehicle_type == "motorcycle":
            print("EHRHERHEHRHE")
            # data = Interface(soup).get(soup).get_data()
            return {"error": "Can't scrape motorcycles yet"}
        else:
            data = {}

        # Add id, url,...
        vehicle_id = extract_url_param(url, "id")
        if not vehicle_id:
            vehicle_id = extract_url_param(url, "ID")
        try:
            data["id"] = int(vehicle_id)
        except ValueError:
            data["id"] = None
        data["url"] = url

        return data


if __name__ == "__main__":
    # url = "https://www.avto.net/Ads/details.asp?id=20032741&display=Suzuki%20Gsxr%201000"
    url = "https://www.avto.net/Ads/details.asp?id=20032640&display=Audi%20A4%20Avant"
    # url = "https://www.avto.net/Ads/details.asp?id=20036370&display=Seat%20Leon"  # Already sold

    # vehicle_data = uc.loop().run_until_complete(scrape_url(url))
    # print(vehicle_data)
    scraper = AvtonetScraper()
    data = scraper.get_vehicle(url)
    print(data)
