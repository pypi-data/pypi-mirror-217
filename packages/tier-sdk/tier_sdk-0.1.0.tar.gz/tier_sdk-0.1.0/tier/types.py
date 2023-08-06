from typing import TypedDict


class VehicleAttributes(TypedDict):
    state: str
    lastLocationUpdate: str
    lastStateChange: str
    batteryLevel: int
    currentRangeMeters: int
    lat: float
    lng: float
    maxSpeed: int
    zoneId: str
    code: int
    isRentable: bool
    iotVendor: str
    licencePlate: str
    vehicleType: str


class Vehicle(TypedDict):
    id: int
    type: str
    attributes: VehicleAttributes


class VehiclesCollection(TypedDict):
    data: list[Vehicle]
