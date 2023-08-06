from typing import Optional, cast

import requests

from .types import VehiclesCollection, RootZonesCollection, RootZone, Vehicle

TIMEOUT = 3
API_BASE_URI = "https://platform.tier-services.io"


class TIERException(RuntimeError):
    """Unknown error"""


class UnauthorizedException(TIERException):
    """Unauthorized"""


class NotFoundException(TIERException):
    """Not Found"""


class TIER:
    def __init__(self, api_token: str, base_uri: str = API_BASE_URI) -> None:
        self.api_token: str = api_token
        self.base_uri: str = base_uri
        self.headers: dict = {"X-API-Key": self.api_token}

        self.vehicles: Vehicles = Vehicles(self)
        self.zones: Zones = Zones(self)

    def get(self, url: str):
        return self.__request("GET", url)

    def post(self, url: str, data: Optional[dict] = None):
        if data is None:
            data = {}
        return self.__request("POST", url, data)

    def __request(self, method: str, url: str, params: Optional[dict] = None):
        if params is None:
            params = {}

        if method == "GET":
            response = requests.get(
                self.base_uri + url, params=params, headers=self.headers
            )
        elif method == "POST":
            response = requests.post(
                self.base_uri + url, json=params, headers=self.headers
            )
        else:
            raise RuntimeError("Invalid request method provided")

        if response.status_code == 401:
            raise UnauthorizedException()
        if response.status_code == 404:
            raise NotFoundException(response.json().get("title"))
        if response.status_code >= 400:
            raise TIERException(response.json().get("error") or "Unknown error")
        return response.json()


class Vehicles:
    def __init__(self, client: TIER):
        self.client = client

    def in_radius(
        self, latitude: float, longitude: float, radius: int
    ) -> VehiclesCollection:
        return cast(
            VehiclesCollection,
            self.client.get(
                f"/v2/vehicle?lat={latitude}&lng={longitude}&radius={radius}"
            ),
        )

    def in_zone(self, zone_id: str) -> VehiclesCollection:
        return cast(
            VehiclesCollection, self.client.get(f"/v2/vehicle?zoneId={zone_id}")
        )

    def get(self, identifier: str) -> Vehicle:
        return cast(
            Vehicle, self.client.get(f"/v1/vehicle/{identifier}").get("data")[0]
        )


class Zones:
    def __init__(self, client: TIER):
        self.client = client

    def all(self) -> RootZonesCollection:
        return cast(RootZonesCollection, self.client.get(f"/v2/zone/root").get("data"))

    def get(self, identifier: str) -> RootZone:
        return cast(
            RootZone, self.client.get(f"/v2/zone/root/{identifier}").get("data")
        )

    def near(self, latitude: float, longitude: float) -> RootZonesCollection:
        return cast(
            RootZonesCollection,
            self.client.get(f"/v2/zone/root?lat={latitude}&lng={longitude}").get(
                "data"
            ),
        )
