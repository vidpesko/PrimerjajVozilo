from urllib.parse import urlparse, parse_qs

import nodriver as uc
from bs4 import BeautifulSoup

from . import parsers
from .schemas import Vehicle


def extract_url_param(url: str, param_key: str):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params.get(param_key, [None])[0]


def get_id(url: str) -> int | None:
    return extract_url_param(url, "id")


def extract_html_data(html: str, vehicle: Vehicle, url: str) -> Vehicle:
    soup = BeautifulSoup(html, 'lxml')

    # Get name
    vehicle.name = extract_url_param(url, "display")

    # Get price
    vehicle.price = parsers.price_parser(
        soup.find("p", {"class": "h2 font-weight-bold align-middle py-4 mb-0"}).string
    )

    return vehicle


async def scrape_url(url: str) -> Vehicle:
    # NAvigate to url and get html content
    browser = await uc.start(
        headless=True,
    )

    page = await browser.get(url)

    html = await page.get_content()

    if not html:
        return {"error": "Website with this url is empty"}

    await page.close()

    # Extract id from url
    avtonet_id = get_id(url)

    # Extract data and load it into pydantic model
    vehicle = Vehicle(url=url, avtonet_id=avtonet_id)
    vehicle = extract_html_data(html, vehicle, url)

    # Return dict of all data
    return vehicle


def run_until_complete(task, url):
    return uc.loop().run_until_complete(scrape_url(url))


if __name__ == "__main__":
    url = "https://www.avto.net/Ads/details.asp?id=19867197&display=Honda%20CB500FA%20CB%20500%20A2%20IZPIT"

    vehicle_data = uc.loop().run_until_complete(scrape_url(url))
    print(vehicle_data)
