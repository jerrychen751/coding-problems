"""
Tag: AI assisted

Train Trip Manager
 
A metro operator tracks every train trip through a `TripManager`. A trip starts at an
origin station, arrives at one or more stations, and finishes with either `end_trip`
or `cancel_trip`. The manager must enforce the operating rules below.
 
    start_trip
        |
        v
    [at origin]
        |  arrive_at_station
        v
    [at station] <-------------+
        |                      |
        +-- arrive_at_station -+
        |
        +-- end_trip -----> [completed]
        |
        +-- cancel_trip --> [cancelled]
 
Origin station --> station 1 --> station 2 --> station 3 --> last station

Rules:

1. One active trip per driver and per train. A driver may operate, and a train may be
   used by, at most one active trip at a time. A trip is active from `start_trip`
   until `end_trip` or `cancel_trip`.
2. Dwell time. After a train arrives at a station, it must stay there for at least
   45 seconds before it can depart or the trip can end, so passengers can get on and
   off.
3. Headway. At any station, a train may not arrive within 3 minutes of the previous
   departure from that station. Exactly 3 minutes after the previous departure is allowed.
   Arrivals made by `start_trip` count.
4. Capacity. A train holds at most 200 passengers, or 250 during rush hour. Rush
   hour is Monday to Friday, 07:00 to 09:30 and 16:30 to 19:00, where each window
   includes its start and excludes its end. Capacity is decided by the arrival time.
   Passengers alight before anyone boards. If not everyone fits, as many board as fit
   and the rest stay on the platform. Nobody is forced off: a train that is over the
   current capacity (for example, it filled up during rush hour) simply accepts no new
   boarders until it is under the limit again. -- fill until the capacity and enforce the rush hour constraint
5. Driver rest. A driver must rest at least 2 minutes between the end of one trip
   and the start of their next trip. (between trips we have at least 2 minute cooldown)
6. Trip lifecycle. A trip starts at its origin station, then arrives at one or more
   stations, and finishes as either completed (`end_trip`) or cancelled
   (`cancel_trip`). A trip can finish only while the train is stopped at a station it
   arrived at after the origin, so a trip that has not yet reached its first station
   can be neither completed nor cancelled.
 
Interfaces:
- start_trip
- arrive_at_station 
- end_trip 
- cancel_trip
 
Ask: Make sure all the rules are enforced
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class TripStatus(Enum):
    AT_STATION = "at_station"
    IN_TRANSIT = "in_transit"
    ENDED = "ended"
    CANCELLED = "cancelled"


@dataclass
class Trip:
    trip_id: str
    train_id: str
    driver_id: str
    last_arrival_time: datetime
    current_station: str
    status: TripStatus = TripStatus.AT_STATION
    passengers: int = 0
    last_departure_time: datetime | None = None


class TripManager:
    # Rule 4: capacity schedule — each entry is (start, end, capacity) as offsets from midnight,
    # Mon–Fri only; start inclusive, end exclusive. Unmatched times fall back to _DEFAULT_CAPACITY.
    _DEFAULT_CAPACITY = 200
    _CAPACITY_SCHEDULE: list[tuple[timedelta, timedelta, int]] = [
        (timedelta(hours=7), timedelta(hours=9, minutes=30), 250),   # morning rush
        (timedelta(hours=16, minutes=30), timedelta(hours=19), 250), # evening rush
    ]

    def __init__(self) -> None:
        self.trips: dict[str, Trip] = {}  # trip_id -> Trip

        # Rule 1
        self._active_by_driver: dict[str, str] = {}  # driver_id -> trip_id
        self._active_by_train: dict[str, str] = {}  # train_id -> trip_id
        # Rule 3
        self._last_departure_by_station: dict[str, datetime] = {}  # station_id -> time
        # Rule 5
        self._last_trip_end_by_driver: dict[str, datetime] = {}  # driver_id -> time

    def _get_capacity_at(self, time: datetime) -> int:
        if time.weekday() < 5:  # Mon–Fri
            offset = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
            for start, end, capacity in self._CAPACITY_SCHEDULE:
                if start <= offset < end:
                    return capacity
        return self._DEFAULT_CAPACITY

    def get_trip(self, trip_id: str) -> Trip:
        if trip_id not in self.trips:
            raise KeyError(f"unknown trip {trip_id}")
        return self.trips[trip_id]

    def start_trip(
        self,
        trip_id: str,
        train_id: str,
        driver_id: str,
        station_id: str,
        time: datetime,
        boarding: int = 0,
    ) -> int:
        if trip_id in self.trips:
            raise ValueError(f"trip {trip_id} already exists")
        if driver_id in self._active_by_driver:
            raise ValueError(f"driver {driver_id} already has an active trip")
        if train_id in self._active_by_train:
            raise ValueError(f"train {train_id} is already on an active trip")
        if boarding < 0:
            raise ValueError("passenger counts must be non-negative")
        # Rule 5: driver rest
        last_end = self._last_trip_end_by_driver.get(driver_id)
        if last_end is not None and time - last_end < timedelta(minutes=2):
            raise ValueError(f"driver {driver_id} has not rested 2 minutes since their last trip")
        # Rule 3: headway check (start_trip arrivals count)
        last_dep = self._last_departure_by_station.get(station_id)
        if last_dep is not None and time - last_dep < timedelta(minutes=3):
            raise ValueError(f"headway violation at {station_id}")

        trip = Trip(
            trip_id=trip_id,
            train_id=train_id,
            driver_id=driver_id,
            last_arrival_time=time,
            current_station=station_id,
        )
        self.trips[trip_id] = trip
        self._active_by_driver[driver_id] = trip_id
        self._active_by_train[train_id] = trip_id

        capacity = self._get_capacity_at(time)
        actual_boarding = min(boarding, capacity)
        trip.passengers = actual_boarding
        return boarding - actual_boarding

    def arrive_at_station(
        self,
        trip_id: str,
        station_id: str,
        time: datetime,
        alighting: int = 0,
        boarding: int = 0,
    ) -> int:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.IN_TRANSIT:
            raise ValueError(f"trip {trip_id} must be in transit to arrive at a station")
        # Rule 3: headway check
        last_dep = self._last_departure_by_station.get(station_id)
        if last_dep is not None and time - last_dep < timedelta(minutes=3):
            raise ValueError(f"headway violation at {station_id}")
        trip.status = TripStatus.AT_STATION
        trip.last_arrival_time = time
        trip.current_station = station_id

        if alighting < 0 or boarding < 0:
            raise ValueError("passenger counts must be non-negative")
        if alighting > trip.passengers:
            raise ValueError("more passengers alighting than on board")

        trip.passengers -= alighting

        # Rule 4: capacity is set by arrival time; over-limit trains accept no new boarders
        capacity = self._get_capacity_at(time)
        if trip.passengers >= capacity:
            return boarding
        actual_boarding = min(boarding, capacity - trip.passengers)
        trip.passengers += actual_boarding
        return boarding - actual_boarding

    def depart_station(self, trip_id: str, station_id: str, time: datetime) -> None:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.AT_STATION:
            raise ValueError(f"trip {trip_id} is not at a station")
        if station_id != trip.current_station:
            raise ValueError(f"trip {trip_id} is at {trip.current_station}, not {station_id}")
        # Rule 2: dwell time
        if time - trip.last_arrival_time < timedelta(seconds=45):
            raise ValueError(f"dwell time not met at {station_id}: train must stay at least 45 seconds")
        trip.last_departure_time = time
        trip.status = TripStatus.IN_TRANSIT
        self._last_departure_by_station[station_id] = time

    def end_trip(self, trip_id: str, time: datetime) -> None:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.AT_STATION:
            raise ValueError(f"trip {trip_id} must be at a station to end")
        # Rule 6: must have departed the origin
        if trip.last_departure_time is None:
            raise ValueError(f"trip {trip_id} has not departed the origin yet")
        # Rule 2: dwell time
        if time - trip.last_arrival_time < timedelta(seconds=45):
            raise ValueError("dwell time not met: train must stay at least 45 seconds before ending")

        trip.status = TripStatus.ENDED
        trip.passengers = 0
        self._active_by_driver.pop(trip.driver_id)
        self._active_by_train.pop(trip.train_id)
        self._last_trip_end_by_driver[trip.driver_id] = time

    def cancel_trip(self, trip_id: str, time: datetime) -> None:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.AT_STATION:
            raise ValueError(f"trip {trip_id} can only be cancelled at a station")
        # Rule 6: must have departed the origin
        if trip.last_departure_time is None:
            raise ValueError(f"trip {trip_id} has not departed the origin yet")
        # Rule 2: dwell time
        if time - trip.last_arrival_time < timedelta(seconds=45):
            raise ValueError("dwell time not met: train must stay at least 45 seconds before cancelling")

        trip.status = TripStatus.CANCELLED
        trip.passengers = 0
        self._active_by_driver.pop(trip.driver_id)
        self._active_by_train.pop(trip.train_id)
        self._last_trip_end_by_driver[trip.driver_id] = time

def main() -> None:
    passed = 0
    failed = 0

    def ok(label: str) -> None:
        nonlocal passed
        passed += 1
        print(f"  PASS  {label}")

    def expect_error(label: str, fn, fragment: str) -> None:
        nonlocal failed
        try:
            fn()
            failed += 1
            print(f"  FAIL  {label} — expected ValueError containing '{fragment}'")
        except ValueError as e:
            if fragment in str(e):
                ok(label)
            else:
                failed += 1
                print(f"  FAIL  {label} — wrong error: {e}")

    WED_NORMAL = datetime(2026, 10, 21, 10, 0)   # Wed 10:00, outside rush
    WED_RUSH_AM = datetime(2026, 10, 21, 8, 0)   # Wed 08:00, morning rush
    WED_RUSH_PM = datetime(2026, 10, 21, 17, 0)  # Wed 17:00, evening rush
    SAT_NORMAL = datetime(2026, 10, 25, 8, 0)    # Sat 08:00, never rush

    def at_station(
        mgr: TripManager,
        trip_id: str = "T1",
        train_id: str = "TR1",
        driver_id: str = "D1",
        origin: str = "A",
        dest: str = "B",
        start: datetime = WED_NORMAL,
    ) -> None:
        """Start a trip and arrive at dest, leaving the trip AT_STATION there."""
        mgr.start_trip(trip_id, train_id, driver_id, origin, start)
        mgr.depart_station(trip_id, origin, start + timedelta(seconds=45))
        mgr.arrive_at_station(trip_id, dest, start + timedelta(minutes=4))

    # Rule 1 — one active trip per driver and per train
    print("Rule 1")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error("duplicate trip ID", lambda: m.start_trip("T1", "TR2", "D2", "B", WED_NORMAL), "already exists")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error("driver already active", lambda: m.start_trip("T2", "TR2", "D1", "B", WED_NORMAL), "already has an active trip")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error("train already active", lambda: m.start_trip("T2", "TR1", "D2", "B", WED_NORMAL), "already on an active trip")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.end_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=45))
    m.start_trip("T2", "TR2", "D1", "C", WED_NORMAL + timedelta(minutes=7))
    ok("driver free after end_trip")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.cancel_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=45))
    m.start_trip("T2", "TR2", "D1", "C", WED_NORMAL + timedelta(minutes=7))
    ok("driver free after cancel_trip")

    # Rule 2 — dwell time (45 seconds)
    print("Rule 2")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    m.depart_station("T1", "A", WED_NORMAL + timedelta(seconds=45))
    ok("depart exactly at 45s")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error("depart too early", lambda: m.depart_station("T1", "A", WED_NORMAL + timedelta(seconds=44)), "dwell time")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.end_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=45))
    ok("end_trip exactly at 45s")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    expect_error("end_trip too early", lambda: m.end_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=44)), "dwell time")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    expect_error("cancel_trip too early", lambda: m.cancel_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=44)), "dwell time")

    # Rule 3 — headway (3 minutes after last departure from a station)
    print("Rule 3")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    m.depart_station("T1", "A", WED_NORMAL + timedelta(seconds=45))
    m.start_trip("T2", "TR2", "D2", "A", WED_NORMAL + timedelta(seconds=45, minutes=3))
    ok("start_trip exactly 3min after departure")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    m.depart_station("T1", "A", WED_NORMAL + timedelta(seconds=45))
    expect_error(
        "start_trip headway violation",
        lambda: m.start_trip("T2", "TR2", "D2", "A", WED_NORMAL + timedelta(minutes=3, seconds=44)),
        "headway",
    )

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.depart_station("T1", "B", WED_NORMAL + timedelta(minutes=4, seconds=45))
    m.start_trip("T2", "TR2", "D2", "C", WED_NORMAL + timedelta(minutes=8))
    m.depart_station("T2", "C", WED_NORMAL + timedelta(minutes=8, seconds=45))
    m.arrive_at_station("T2", "B", WED_NORMAL + timedelta(minutes=7, seconds=45))
    ok("arrive_at_station exactly 3min after departure")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.depart_station("T1", "B", WED_NORMAL + timedelta(minutes=4, seconds=45))
    m.start_trip("T2", "TR2", "D2", "C", WED_NORMAL + timedelta(minutes=8))
    m.depart_station("T2", "C", WED_NORMAL + timedelta(minutes=8, seconds=45))
    expect_error(
        "arrive_at_station headway violation",
        lambda: m.arrive_at_station("T2", "B", WED_NORMAL + timedelta(minutes=7, seconds=44)),
        "headway",
    )

    # Rule 4 — capacity
    print("Rule 4")

    m = TripManager()
    left = m.start_trip("T1", "TR1", "D1", "A", SAT_NORMAL, boarding=200)
    assert left == 0 and m.get_trip("T1").passengers == 200
    ok("normal capacity on weekend, exact fill")

    m = TripManager()
    left = m.start_trip("T1", "TR1", "D1", "A", SAT_NORMAL, boarding=210)
    assert left == 10 and m.get_trip("T1").passengers == 200
    ok("normal capacity overflow returns leftover")

    m = TripManager()
    left = m.start_trip("T1", "TR1", "D1", "A", WED_RUSH_AM, boarding=250)
    assert left == 0 and m.get_trip("T1").passengers == 250
    ok("rush capacity morning, exact fill")

    m = TripManager()
    left = m.start_trip("T1", "TR1", "D1", "A", WED_RUSH_PM, boarding=260)
    assert left == 10 and m.get_trip("T1").passengers == 250
    ok("rush capacity evening overflow returns leftover")

    m = TripManager()
    left = m.start_trip("T1", "TR1", "D1", "A", datetime(2026, 10, 21, 7, 0), boarding=250)
    assert left == 0
    ok("rush boundary 07:00 inclusive")

    m = TripManager()
    left = m.start_trip("T1", "TR1", "D1", "A", datetime(2026, 10, 21, 9, 30), boarding=210)
    assert left == 10
    ok("rush boundary 09:30 exclusive")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", SAT_NORMAL, boarding=190)
    m.depart_station("T1", "A", SAT_NORMAL + timedelta(seconds=45))
    # 50 alight → 140 on board; 70 want to board; cap 200 → 60 board, 10 left
    left = m.arrive_at_station("T1", "B", SAT_NORMAL + timedelta(minutes=4), alighting=50, boarding=70)
    assert left == 10 and m.get_trip("T1").passengers == 200
    ok("alighting before boarding, partial fill")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", SAT_NORMAL, boarding=200)
    m.depart_station("T1", "A", SAT_NORMAL + timedelta(seconds=45))
    left = m.arrive_at_station("T1", "B", SAT_NORMAL + timedelta(minutes=4), boarding=30)
    assert left == 30 and m.get_trip("T1").passengers == 200
    ok("at capacity, all boarders left on platform")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_RUSH_AM, boarding=250)
    m.depart_station("T1", "A", WED_RUSH_AM + timedelta(seconds=45))
    left = m.arrive_at_station("T1", "B", datetime(2026, 10, 21, 10, 0), boarding=5)
    assert left == 5 and m.get_trip("T1").passengers == 250
    ok("overfilled rush train accepts no boarders in normal hours")

    # Rule 5 — driver rest (2 minutes)
    print("Rule 5")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    ok("first trip, no rest required")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    end_time = WED_NORMAL + timedelta(minutes=4, seconds=45)
    m.end_trip("T1", end_time)
    m.start_trip("T2", "TR2", "D1", "C", end_time + timedelta(minutes=2))
    ok("exact 2min rest after end_trip")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    end_time = WED_NORMAL + timedelta(minutes=4, seconds=45)
    m.end_trip("T1", end_time)
    expect_error(
        "too soon after end_trip",
        lambda: m.start_trip("T2", "TR2", "D1", "C", end_time + timedelta(minutes=1, seconds=59)),
        "not rested",
    )

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    end_time = WED_NORMAL + timedelta(minutes=4, seconds=45)
    m.cancel_trip("T1", end_time)
    expect_error(
        "too soon after cancel_trip",
        lambda: m.start_trip("T2", "TR2", "D1", "C", end_time + timedelta(minutes=1, seconds=59)),
        "not rested",
    )

    # Rule 6 — trip lifecycle
    print("Rule 6")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error("end_trip before departing origin", lambda: m.end_trip("T1", WED_NORMAL + timedelta(minutes=1)), "not departed")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error("cancel_trip before departing origin", lambda: m.cancel_trip("T1", WED_NORMAL + timedelta(minutes=1)), "not departed")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.end_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=45))
    assert m.get_trip("T1").status == TripStatus.ENDED
    ok("end_trip after arriving at non-origin station")

    m = TripManager()
    at_station(m, start=WED_NORMAL)
    m.cancel_trip("T1", WED_NORMAL + timedelta(minutes=4, seconds=45))
    assert m.get_trip("T1").status == TripStatus.CANCELLED
    ok("cancel_trip after arriving at non-origin station")

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    expect_error(
        "arrive_at_station when not in transit",
        lambda: m.arrive_at_station("T1", "B", WED_NORMAL + timedelta(minutes=4)),
        "must be in transit",
    )

    m = TripManager()
    m.start_trip("T1", "TR1", "D1", "A", WED_NORMAL)
    m.depart_station("T1", "A", WED_NORMAL + timedelta(seconds=45))
    expect_error(
        "depart_station when in transit",
        lambda: m.depart_station("T1", "B", WED_NORMAL + timedelta(minutes=2)),
        "not at a station",
    )

    print(f"\n{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
