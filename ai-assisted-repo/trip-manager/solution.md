Tag: AI assisted

# Designing a Train Trip Manager

## Design decisions
1. The manager adds a fifth call, `depart_station(trip_id, at)`. The dwell rule limits when a train may depart, and the headway rule measures from the last departure at a station, so the model needs the departure time. The four calls in the spec never record it. Inferring the departure from the next arrival would also be wrong, because the train left the previous station some time before it reached the next one.
2. Each trip moves through five states: `AT_ORIGIN`, `IN_TRANSIT`, `AT_STATION`, `COMPLETED` and `CANCELLED`. Giving the origin its own state turns rule 6 into a single status check: a trip in `AT_ORIGIN` cannot finish, and a trip can only reach `AT_STATION` by departing and arriving somewhere.
3. Every call runs all of its checks before it changes anything. A rejected call leaves the trip, the driver, the train and the station exactly as they were, so the caller can fix the input and retry.
4. Each rule reads one dictionary, keyed by the thing the rule is about: active trips by driver and by train (rule 1), the last departure by station (rule 3), and the last finish by driver (rule 5). Every call does a constant number of dictionary lookups, so every operation is O(1).
5. A rule violation raises `ValueError` with a message that names the rule. An unknown trip ID raises `KeyError`.

## Classes, Interfaces and Enumerations
1. The **TripStatus** enum lists the five states above.
2. The **Trip** dataclass holds one trip: its train, driver, current or last station, status, passenger count, and `last_event_at`, the time of its latest arrival or departure.
3. The **TripManager** class owns every trip and the per-rule indexes. Its public calls are `start_trip`, `depart_station`, `arrive_at_station`, `end_trip` and `cancel_trip`.
4. `start_trip` and `arrive_at_station` return the number of passengers left on the platform.
5. `end_trip` and `cancel_trip` share one private `_finish` method and differ only in the final status.

## How each rule is enforced
1. One active trip. `start_trip` rejects a driver or train already in `active_trip_by_driver` or `active_trip_by_train`. `_finish` removes both entries.
2. Dwell time. `depart_station`, `end_trip` and `cancel_trip` reject a time less than 45 seconds after the latest arrival. For a trip still at its origin, `start_trip` counts as that arrival.
3. Headway. `start_trip` and `arrive_at_station` reject a time less than 3 minutes after `last_departure_by_station[station]`. Exactly 3 minutes passes because the check uses `<`.
4. Capacity. `_board` picks 250 on a weekday inside a rush window and 200 otherwise, using the arrival time. `arrive_at_station` removes alighting passengers before `_board` runs. `max(0, capacity - passengers)` gives an overfull train zero free seats without forcing anyone off.
5. Driver rest. `_finish` records `last_finish_by_driver`, and `start_trip` rejects a start less than 2 minutes later. Ending and cancelling both count.
6. Lifecycle. `_finish` rejects `AT_ORIGIN` with "has not reached its first station", and rejects `IN_TRANSIT` or an already finished trip with "is not stopped at a station". `arrive_at_station` accepts only `IN_TRANSIT`, and also rejects an arrival time earlier than the departure.

## Questions to raise with the interviewer
1. May a train arrive at a station where another train is still stopped? The headway rule only measures from a departure, so this model allows it. A stricter model would keep an index of the trip occupying each station and reject the arrival.
2. Does ending a trip clear the platform for the headway rule? The spec does not say. This model records no departure when a trip ends, so the next train's headway is measured from the last real departure.
3. Should more people alight than are on board be an error or be clamped? This model raises, because the count most likely comes from a bad sensor reading that the caller should see.

## Python Implementation

```python
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum


class TripStatus(Enum):
    AT_ORIGIN = "at_origin"
    IN_TRANSIT = "in_transit"
    AT_STATION = "at_station"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Trip:
    trip_id: str
    train_id: str
    driver_id: str
    station_id: str  # the station the train is stopped at, or the one it last left
    last_event_at: datetime  # time of the latest arrival or departure
    status: TripStatus = TripStatus.AT_ORIGIN
    passengers: int = 0


class TripManager:
    MIN_DWELL = timedelta(seconds=45)
    MIN_HEADWAY = timedelta(minutes=3)
    MIN_DRIVER_REST = timedelta(minutes=2)
    STANDARD_CAPACITY = 200
    RUSH_HOUR_CAPACITY = 250
    # Monday to Friday only; each window includes its start and excludes its end.
    RUSH_HOURS = ((time(7, 0), time(9, 30)), (time(16, 30), time(19, 0)))

    def __init__(self) -> None:
        self.trips: dict[str, Trip] = {}
        self.active_trip_by_driver: dict[str, str] = {}
        self.active_trip_by_train: dict[str, str] = {}
        self.last_departure_by_station: dict[str, datetime] = {}
        self.last_finish_by_driver: dict[str, datetime] = {}

    def start_trip(
        self,
        trip_id: str,
        train_id: str,
        driver_id: str,
        station_id: str,
        at: datetime,
        boarding: int = 0,
    ) -> int:
        if trip_id in self.trips:
            raise ValueError(f"trip {trip_id} already exists")
        if driver_id in self.active_trip_by_driver:
            raise ValueError(f"driver {driver_id} already has an active trip")
        if train_id in self.active_trip_by_train:
            raise ValueError(f"train {train_id} already has an active trip")
        last_finish = self.last_finish_by_driver.get(driver_id)
        if last_finish is not None and at - last_finish < self.MIN_DRIVER_REST:
            raise ValueError(f"driver {driver_id} has not rested {self.MIN_DRIVER_REST} since their last trip")
        self._check_headway(station_id, at)
        if boarding < 0:
            raise ValueError("passenger counts must be non-negative")

        trip = Trip(trip_id, train_id, driver_id, station_id, at)
        self.trips[trip_id] = trip
        self.active_trip_by_driver[driver_id] = trip_id
        self.active_trip_by_train[train_id] = trip_id
        return self._board(trip, at, boarding)

    def _check_headway(self, station_id: str, at: datetime) -> None:
        last_departure = self.last_departure_by_station.get(station_id)
        if last_departure is not None and at - last_departure < self.MIN_HEADWAY:
            raise ValueError(f"headway violation at {station_id}: last departure was at {last_departure}")

    def _board(self, trip: Trip, at: datetime, boarding: int) -> int:
        # Capacity is set by the arrival time. A train already over it keeps its passengers and takes nobody new.
        is_rush_hour = at.weekday() < 5 and any(start <= at.time() < end for start, end in self.RUSH_HOURS)
        capacity = self.RUSH_HOUR_CAPACITY if is_rush_hour else self.STANDARD_CAPACITY
        boarded = min(boarding, max(0, capacity - trip.passengers))
        trip.passengers += boarded
        return boarding - boarded

    def depart_station(self, trip_id: str, at: datetime) -> None:
        trip = self._get_trip(trip_id)
        if trip.status not in (TripStatus.AT_ORIGIN, TripStatus.AT_STATION):
            raise ValueError(f"trip {trip_id} is not stopped at a station")
        self._check_dwell(trip, at)

        trip.status = TripStatus.IN_TRANSIT
        trip.last_event_at = at
        self.last_departure_by_station[trip.station_id] = at

    def _get_trip(self, trip_id: str) -> Trip:
        if trip_id not in self.trips:
            raise KeyError(f"unknown trip {trip_id}")
        return self.trips[trip_id]

    def _check_dwell(self, trip: Trip, at: datetime) -> None:
        if at - trip.last_event_at < self.MIN_DWELL:
            raise ValueError(f"trip {trip.trip_id} must dwell {self.MIN_DWELL} at {trip.station_id}")

    def arrive_at_station(
        self,
        trip_id: str,
        station_id: str,
        at: datetime,
        alighting: int = 0,
        boarding: int = 0,
    ) -> int:
        trip = self._get_trip(trip_id)
        if trip.status != TripStatus.IN_TRANSIT:
            raise ValueError(f"trip {trip_id} must be in transit to arrive at a station")
        if at < trip.last_event_at:
            raise ValueError(f"trip {trip_id} cannot arrive before it departed")
        self._check_headway(station_id, at)
        if alighting < 0 or boarding < 0:
            raise ValueError("passenger counts must be non-negative")
        if alighting > trip.passengers:
            raise ValueError(f"only {trip.passengers} passengers are on board")

        trip.status = TripStatus.AT_STATION
        trip.station_id = station_id
        trip.last_event_at = at
        trip.passengers -= alighting
        return self._board(trip, at, boarding)

    def end_trip(self, trip_id: str, at: datetime) -> None:
        self._finish(trip_id, at, TripStatus.COMPLETED)

    def _finish(self, trip_id: str, at: datetime, outcome: TripStatus) -> None:
        trip = self._get_trip(trip_id)
        if trip.status == TripStatus.AT_ORIGIN:
            raise ValueError(f"trip {trip_id} has not reached its first station")
        if trip.status != TripStatus.AT_STATION:
            raise ValueError(f"trip {trip_id} is not stopped at a station")
        self._check_dwell(trip, at)

        trip.status = outcome
        del self.active_trip_by_driver[trip.driver_id]
        del self.active_trip_by_train[trip.train_id]
        self.last_finish_by_driver[trip.driver_id] = at

    def cancel_trip(self, trip_id: str, at: datetime) -> None:
        self._finish(trip_id, at, TripStatus.CANCELLED)
```
