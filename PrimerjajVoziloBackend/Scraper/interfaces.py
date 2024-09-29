from .schemas import CAR_EXTRACTION_PLAN
# from schemas import CAR_EXTRACTION_PLAN


class Interface:
    def __init__(self, soup) -> None:
        self.soup = soup

    def get_data(self, plan) -> dict:
        data = {}

        for override_func in plan["overrides"]:
            data.update(override_func(self.soup))

        for key, value in plan["elements"].items():
            if value.get("override", False):
                try:
                    data[key] = value["override"](self.soup)
                except Exception:
                    data[key] = None
            else:
                for identifier in value["identifiers"]:
                    try:
                        element = self.soup.find(value["tag"], identifier)
                        element_value = "".join(list(element.stripped_strings))
                        data[key] = element_value
                    except Exception:
                        data[key] = None
                    finally:
                        if data[key]:
                            break

        return data