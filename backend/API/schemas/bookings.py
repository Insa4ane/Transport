from pydantic import BaseModel, ConfigDict


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seats: int
    ride_id: int
    origin: str
    destination: str
    departure: str
    price: float
    driver_name: str
