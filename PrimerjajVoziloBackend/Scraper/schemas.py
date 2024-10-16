import re

from bs4 import BeautifulSoup, Tag

from .utils import remove_repeated_spaces

# from utils import remove_repeated_spaces


# Override functions
def get_images(soup: BeautifulSoup) -> list:
    container = soup.find("div", id="lightgallery")
    images = []
    for p_element in container.children:
        if p_element == "\n":
            continue

        img = p_element.img
        try:
            src = img["src"]
        except KeyError:
            src = img["data-cookieblock-src"]
        src = src.replace("_small", "")
        images.append(src)

    return images


def get_description(soup: BeautifulSoup) -> str:
    element = soup.find("div", id="StareOpombe")
    desc = str(element)
    # Structure text
    desc = desc.replace(
        '<div class="col-12 p-0 font-weight-normal overflow-hidden" id="StareOpombe">',
        "",
    )
    desc = desc.replace("</div>", "")
    # desc = desc.replace("<br/>", "\n")
    desc = re.sub(r"<br/>\s*<br/>+", "<br/>", desc)
    # desc = desc.replace("/n", "<br/>")
    desc = remove_repeated_spaces(desc)
    return desc


def get_name(soup: BeautifulSoup) -> str:
    element = soup.find(
        "div",
        {
            "class": "container bg-white GO-Rounded-B GO-Shadow-B m-0 pb-3 mb-3 sticky-top"
        },
    ).div.div.h3

    name = " ".join(list(element.stripped_strings))
    return remove_repeated_spaces(name)


def get_neto_price(soup: BeautifulSoup) -> str:
    element = soup.find(
        "p",
        {
            "class": "h5 font-weight-bold text-muted"
        }
    ).stripped_strings

    value = "".join(list(element))
    value = value.replace("oz. ", "")
    return value


def get_seller_type(soup: BeautifulSoup) -> str:
    try:
        phone_num = soup.find("p", {"class": "h3 font-weight-bold m-0"})
    except Exception:
        phone_num = None

    return "person" if phone_num else "company"


CAR_HEADER_NAMES_MAP = {
    "Prva registracija": "firstRegistration",
    "Prevoženi km": "mileage",
    "Lastnikov": "numOfOwners",
    "Kraj ogleda": "location",
    "Moč motorja": "power",
}


def get_table_properties(soup: BeautifulSoup, headers_names_map: dict, validation_func):
    data = {}
    container = soup.find("table", {"class": "table table-sm"}).tbody

    for row in container.children:
        if isinstance(row, Tag):
            header = row.th.string
            if not header:
                continue
            header = str(header)

            if not list(row.td.stripped_strings):
                continue

            # Strip value
            value = str(list(row.td.stripped_strings)[0])
            value = remove_repeated_spaces(value)
            if not value:
                continue

            new_header = headers_names_map.get(header[:-1], header[:-1])

            # Vehicle specific validations / modifications: function takes current header and value as parameters. It then modifies value (if needed) and returns value.
            # It also accepts data dictionary, and modifies it, if needed
            value = validation_func(data, new_header, value)
            
            if not new_header:
                continue
            data[new_header] = value
    return data


def get_car_table_properties(soup: BeautifulSoup) -> dict:
    def validation(data: dict, header: str, value: str) -> str:
        if header == "Motor":
            if value[-2:] == "kw":
                engine_power = value
            else:
                try:
                    engine_power = value.split(",")[0]
                except IndexError:
                    engine_power = value
            engine_power = engine_power.replace("\n", "")
            data["power"] = engine_power
        # If location is not specified (in case of company seller), do not put "," as location
        elif (header == "location") and (value == ","):
            try:
                el = soup.find("a", {"data-target": "#MapModal"})
                value = "".join(list(el.stripped_strings))
            except Exception:
                value = None
        return value

    return get_table_properties(soup, CAR_HEADER_NAMES_MAP, validation)


# Common extraction plan, shared on all vehicles
EXTRACTION_PLAN = {
    "overrides": [],
    "elements": {
        "price": {
            "tag": "p",
            "identifiers": [
                {"class": "h2 font-weight-bold align-middle py-4 mb-0"},
                {"class": "h2 font-weight-bold text-danger mb-3"},
            ],
        },
        "images": {"override": get_images},
        "description": {"override": get_description},
        "name": {"override": get_name},
        "phoneNumber": {
            "tag": "p",
            "identifiers": [
                {"class": "h3 font-weight-bold m-0"},
            ],
        },
        "Stara cena": {
            "tag": "p",
            "identifiers": [
                {
                    "class": "h2 GO-OglasDataStaraCena GO-grayX11 font-weight-bold mb-0 mt-2"
                },
            ],
        },
        "Neto cena": {"override": get_neto_price},
        "seller": {"override": get_seller_type},
    },
}


# Vehicle specific plans
CAR_EXTRACTION_PLAN = {
    **EXTRACTION_PLAN,
    "overrides": [get_car_table_properties]
}


MOTORCYCLE_EXTRACTION_PLAN = {
    **EXTRACTION_PLAN,
    "overrides": [get_car_table_properties]
}