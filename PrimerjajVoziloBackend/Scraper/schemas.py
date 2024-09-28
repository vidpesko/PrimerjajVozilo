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
    desc = desc.replace('<div class="col-12 p-0 font-weight-normal overflow-hidden" id="StareOpombe">', "")
    desc = desc.replace("</div>", "")
    # desc = desc.replace("<br/>", "\n")
    desc = re.sub(r'<br/>\s*<br/>+', '<br/>', desc)
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

HEADER_NAMES_MAP = {
    "Prva registracija": "firstRegistration",
    "Prevoženi km": "mileage",
    "Lastnikov": "numOfOwners",
    "Kraj ogleda": "location",
    "Moč motorja": "power",
}

def get_big_data(soup) -> dict:
    container = soup.find("div", {"class": "col-12 bg-white mb-3 p-0 px-2 GO-Rounded GO-Shadow-B"})
    data = {}
    if not container:
        return data
    boxes = container.find_all("div", {"class": "col-6"})
    for box in boxes:
        text = list(box.stripped_strings)
        box_description = HEADER_NAMES_MAP.get(text[0], text[0])
        box_value = "".join(text[1:])
        data[box_description] = box_value
    return data

def get_table_properties(soup: BeautifulSoup) -> dict:
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
            value = str(list(row.td.stripped_strings)[0])
            value = " ".join(value.split())

            if value == "":
                continue

            new_header = HEADER_NAMES_MAP.get(header[:-1], header[:-1])
            if new_header == "Motor":
                if value[-2:] == "kw":
                    engine_power = value
                else:
                    try:
                        engine_power = value.split(",")[0]
                    except IndexError:
                        engine_power = value
                data["power"] = engine_power
            if not new_header:
                continue
            data[new_header] = value
    return data


CAR_EXTRACTION_PLAN = {
    "overrides": [get_table_properties],
    "elements": {
        "price": {
            "tag": "p",
            "identifiers": {"class": "h2 font-weight-bold align-middle py-4 mb-0"},
        },
        "images": {"override": get_images},
        "description": {"override": get_description},
        "name": {"override": get_name},
        "phoneNumber": {
            "tag": "p",
            "identifiers": {"class": "h3 font-weight-bold m-0"},
        },
    },
}
