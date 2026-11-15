from fastapi import APIRouter, Depends, Query

from Database.models import User

from .. import config
from ..dependencies import (
    get_current_user,
    get_ride_service,
    require_driver,
    require_passenger,
)
from ..schemas.rides import BookIn, RideIn, RideOut
from ..services.ride_service import RideService

router = APIRouter(prefix="/rides", tags=["rides"])


@router.get("", response_model=list[RideOut])
def list_rides(
    origin: str = Query("", max_length=config.CITY_MAX),
    destination: str = Query("", max_length=config.CITY_MAX),
    rides: RideService = Depends(get_ride_service),
):
    return rides.list_rides(origin, destination)


@router.get("/{ride_id}", response_model=RideOut)
def get_ride(
    ride_id: int,
    user: User = Depends(get_current_user),
    rides: RideService = Depends(get_ride_service),
):
    return rides.get_ride(ride_id)


@router.post("", response_model=RideOut, status_code=201)
def create_ride(
    data: RideIn,
    driver: User = Depends(require_driver),
    rides: RideService = Depends(get_ride_service),
):
    return rides.create_ride(driver, **data.model_dump())


@router.post("/{ride_id}/book", response_model=RideOut)
def book_ride(
    ride_id: int,
    data: BookIn,
    passenger: User = Depends(require_passenger),
    rides: RideService = Depends(get_ride_service),
):
    return rides.book_ride(ride_id, passenger, data.seats)
