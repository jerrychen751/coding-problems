"""
# Designing a Parking Lot System

## Requirements
1. The parking lot should have multiple levels, each level with a certain number of parking spots.
2. The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
3. Each parking spot should be able to accommodate a specific type of vehicle.
4. The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
5. The system should track the availability of parking spots and provide real-time information to customers.
6. The system should handle multiple entry and exit points and support concurrent access.
"""


from abc import ABC
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict
import threading

class ParkingSpotStatus(Enum):
    AVAILABLE = 1
    OCCUPIED = 2

class VehicleType(Enum):
    CAR = 1
    SEMI = 2
    TRUCK = 3

@dataclass
class Vehicle:
    license_plate: str
    type: VehicleType


class ParkingLot:
    def __init__(self, levels: list[ParkingLevel]) -> None:
        self.levels = levels
        self.vehicles: dict[str, ParkingLevel | None] = {} # license plate -> parking level

        self._lock = threading.Lock()

    def enter(self, vehicle: Vehicle) -> ParkingSpot | None:
        with self._lock:
            if vehicle.license_plate in self.vehicles:
                return None
            self.vehicles[vehicle.license_plate] = None # reserves the license plate so that another concurrent enter() won't work

        for level in self.levels:
            spot = level.enter(vehicle)
            if spot is None:
                continue
            with self._lock:
                self.vehicles[vehicle.license_plate] = level
            return spot

        with self._lock:
            del self.vehicles[vehicle.license_plate]
        return None

    def exit(self, vehicle: Vehicle) -> ParkingSpot | None:
        with self._lock:
            level = self.vehicles.get(vehicle.license_plate)
            if level is None: # Either vehicle is not in parking lot or it's reserved currently for enter() by another thread
                return None
            del self.vehicles[vehicle.license_plate]
        return level.exit(vehicle)

    def get_availability(self) -> dict[int, dict[VehicleType, int]]:
        # Return {level: {vehicle_type: n_spots}}
        availability: dict[int, dict[VehicleType, int]] = {}
        for i in range(len(self.levels)):
            availability[i] = self.levels[i].get_availability()
        return availability


class ParkingLevel:
    def __init__(self, spots: list[ParkingSpot]) -> None:
        self.available: dict[VehicleType, dict[int, ParkingSpot]] = {}
        self.occupied: dict[str, ParkingSpot] = {} # license place -> parking spot
        self._lock = threading.Lock()
        for spot in spots:
            for type in spot.supported_types:
                if type not in self.available:
                    self.available[type] = {}
                self.available[type][spot.id] = spot

    def enter(self, vehicle: Vehicle) -> ParkingSpot | None:
        with self._lock:
            if vehicle.license_plate in self.occupied:
                return None

            spots = self.available.get(vehicle.type)
            if spots is None or len(spots) == 0:
                return None

            spot_id, spot = next(iter(spots.items()))
            spot.occupy(vehicle)
            self.occupied[vehicle.license_plate] = spot
            for type in spot.supported_types:
                self.available[type].pop(spot_id, None)
            return spot

    def exit(self, vehicle: Vehicle) -> ParkingSpot | None:
        with self._lock:
            spot = self.occupied.pop(vehicle.license_plate, None)
            if spot is None:
                return None

            spot.free()
            for type in spot.supported_types:
                self.available[type][spot.id] = spot
            return spot

    def get_availability(self) -> dict[VehicleType, int]:
        with self._lock:
            availability = {}
            for type, spots in self.available.items():
                availability[type] = len(spots)
        return availability


class ParkingSpot:
    def __init__(self, id: int, supported_types: set[VehicleType]) -> None:
        self.id = id
        self.supported_types = supported_types
        self.status = ParkingSpotStatus['AVAILABLE']
        self.vehicle = None

    def occupy(self, vehicle: Vehicle) -> bool:
        if vehicle.type in self.supported_types and self.status == ParkingSpotStatus['AVAILABLE']:
            self.vehicle = vehicle
            self.status = ParkingSpotStatus['OCCUPIED']
            return True

        return False

    def free(self) -> bool:
        if self.status == ParkingSpotStatus['OCCUPIED']:
            self.vehicle = None
            self.status = ParkingSpotStatus['AVAILABLE']
            return True

        return False

