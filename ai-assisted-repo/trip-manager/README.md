Tag: AI assisted

# Designing a Train Trip Manager

A metro operator tracks every train trip through a `TripManager`. A trip starts at an origin station, arrives at one or more stations, and finishes with either `end_trip` or `cancel_trip`. The manager must enforce the operating rules below.

```
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
```

## Requirements
1. One active trip per driver and per train. A driver may operate, and a train may be used by, at most one active trip at a time. A trip is active from `start_trip` until `end_trip` or `cancel_trip`.
2. Dwell time. After a train arrives at a station, it must stay there for at least 45 seconds before it can depart or the trip can end, so passengers can get on and off.
3. Headway. At any station, a train may not arrive within 3 minutes of the previous departure from that station. Exactly 3 minutes after the previous departure is allowed. Arrivals made by `start_trip` count.
4. Capacity. A train holds at most 200 passengers, or 250 during rush hour. Rush hour is Monday to Friday, 07:00 to 09:30 and 16:30 to 19:00, where each window includes its start and excludes its end. Capacity is decided by the arrival time. Passengers alight before anyone boards. If not everyone fits, as many board as fit and the rest stay on the platform. Nobody is forced off: a train that is over the current capacity (for example, it filled up during rush hour) simply accepts no new boarders until it is under the limit again.
5. Driver rest. A driver must rest at least 2 minutes between the end of one trip and the start of their next trip.
6. Trip lifecycle. A trip starts at its origin station, then arrives at one or more stations, and finishes as either completed (`end_trip`) or cancelled (`cancel_trip`). A trip can finish only while the train is stopped at a station it arrived at after the origin, so a trip that has not yet reached its first station can be neither completed nor cancelled.

## Interface
- `start_trip`
- `arrive_at_station`
- `end_trip`
- `cancel_trip`

Make sure every rule is enforced.
