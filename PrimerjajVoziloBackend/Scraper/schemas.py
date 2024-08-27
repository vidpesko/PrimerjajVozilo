from pydantic import BaseModel


class Vehicle(BaseModel):
    avtonet_id: int | None = None
    url: str | None = None
    name: str | None = None
    price: int | None = None