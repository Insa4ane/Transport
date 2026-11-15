from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from .. import config
from ..timeutils import as_utc, now_utc

City = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=config.CITY_MIN, max_length=config.CITY_MAX),
]


class RideIn(BaseModel):
    origin: City
    destination: City
    departure: datetime
    seats: int = Field(ge=1, le=config.MAX_SEATS)
    price: float = Field(ge=0, le=config.MAX_PRICE)

    @model_validator(mode="after")
    def check_ride(self):
        if self.origin.casefold() == self.destination.casefold():
            raise ValueError("Miejsce startu i celu muszą być różne")
        if as_utc(self.departure) <= now_utc():
            raise ValueError("Data odjazdu musi być w przyszłości")
        return self


class BookIn(BaseModel):
    seats: int = Field(ge=1, le=config.MAX_SEATS)


class RideOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    origin: str
    destination: str
    departure: str
    seats_left: int
    price: float
    driver_name: str
