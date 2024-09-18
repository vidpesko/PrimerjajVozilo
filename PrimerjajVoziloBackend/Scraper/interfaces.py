from .schemas import CAR_EXTRACTION_PLAN
# from schemas import CAR_EXTRACTION_PLAN


class Interface:
    def __init__(self, soup) -> None:
        self.soup = soup

        self.plan = None

    def get_data(self) -> dict:
        if not self.plan:
            return "'plan' attr not set"

        data = {}

        for override_func in self.plan["overrides"]:
            data.update(override_func(self.soup))

        for key, value in self.plan["elements"].items():
            if value.get("override", False):
                try:
                    data[key] = value["override"](self.soup)
                except Exception:
                    data[key] = None
            else:
                try:
                    element = self.soup.find(value["tag"], value["identifiers"])
                    element_value = "".join(list(element.stripped_strings))
                    data[key] = element_value
                except Exception:
                    data[key] = None

        return data


class CarInterface(Interface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.plan = CAR_EXTRACTION_PLAN


class MotorcycleInterface(Interface):
    pass
