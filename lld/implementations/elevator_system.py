'''
# Designing an Elevator System

## Requirements
1. The elevator system should consist of multiple elevators serving multiple floors.
2. Each elevator should have a capacity limit and should not exceed it.
3. Users should be able to request an elevator from any floor and select a destination floor.
4. The elevator system should efficiently handle user requests and optimize the movement of elevators to minimize waiting time.
5. The system should prioritize requests based on the direction of travel and the proximity of the elevators to the requested floor.
6. The elevators should be able to handle multiple requests concurrently and process them in an optimal order.
'''

'''
Assumptions:
- Request is per-person
- Integer timestamp (ts) ticks; 1 tick per floor
- After completing a trip if no new requests are assigned wait at floor 0; no basement or lower floors
'''

'''
Elevator System: determine where each elevator should be going, handle requests, plan route for elevators
Elevator: capacity
Request: start_floor, end_floor

Scheduling Algorithm:
- Direction of elevator and request must be the same
- Start floor of request must be within elevator's current path
- If multiple fulfill this requirement then pick elevator at nearest floor currently
- If none fulfill this request then wait for some elevator to finish

The elevator should be given all information needed to manage its own state without ElevatorSystem controlling its tick updates.

Let requests be a list of requests with associated timestamp; system ticks forward time in run simulation
'''


from collections import deque
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    REST = 3


@dataclass
class Request:
    start_floor: int
    end_floor: int
    ts: int
    dir: Direction = field(init=False)

    def __post_init__(self) -> None:
        self.dir = Direction.UP if self.start_floor < self.end_floor else Direction.DOWN


class Elevator:
    _counter = 0

    def __init__(self, max_capacity: int) -> None:
        # Elevator identity
        self.id = Elevator._counter
        Elevator._counter += 1
        self.max_capacity = max_capacity

        # Elevator motion
        self.curr_floor = 0
        self.dir = Direction.REST
        self.riders: list[Request] = [] # curr rider requests
        self.reserved: list[Request] = [] # requests for reserved riders assigned to elevator

    # First deal with request, then tick
    def tick(self) -> None:
        # First update riders/reserved, then reassess direction, then move for the time tick
        self.riders = [r for r in self.riders if r.end_floor != self.curr_floor] + [r for r in self.reserved if r.start_floor == self.curr_floor]
        self.reserved = [r for r in self.reserved if r.start_floor != self.curr_floor]

        stops = [r.start_floor for r in self.reserved] + [r.end_floor for r in self.riders] or [0] # ground floor if no reserved or rider requests
        has_stops_above = any(s > self.curr_floor for s in stops)
        has_stops_below = any(s < self.curr_floor for s in stops)
        if self.dir == Direction.UP and not has_stops_above:
            self.dir = Direction.DOWN if has_stops_below else Direction.REST
        elif self.dir == Direction.DOWN and not has_stops_below:
            self.dir = Direction.UP if has_stops_above else Direction.REST
        elif self.dir == Direction.REST: # idle at floor 0 or happens to be at floor x when request comes in for x -> y
            if has_stops_above:
                self.dir = Direction.UP
            elif has_stops_below:
                self.dir = Direction.DOWN

        if self.dir == Direction.UP:
            self.curr_floor += 1
        elif self.dir == Direction.DOWN:
            self.curr_floor -= 1

    # Invariant: Reserved request must be in same direction + cannot exceed capacity OR elevator is idle
    def can_reserve_ride(self, req: Request) -> bool:
        if self.dir == Direction.REST or len(self.riders) + len(self.reserved) == 0:
            return True
        
        if req.dir != self.dir or any(r.dir != req.dir for r in self.riders + self.reserved):
            return False

        if req.dir == Direction.UP:
            if req.start_floor < self.curr_floor:
                return False
            for floor in range(req.start_floor, req.end_floor):
                num_riders = 0
                for r in self.riders + self.reserved:
                    num_riders += 1 if r.start_floor <= floor < r.end_floor else 0
                if num_riders >= self.max_capacity:
                    return False
        else:
            if req.start_floor > self.curr_floor:
                return False
            for floor in range(req.start_floor - 1, req.end_floor - 1, -1):
                num_riders = 0
                for r in self.riders + self.reserved:
                    num_riders += 1 if r.end_floor <= floor < r.start_floor else 0
                if num_riders >= self.max_capacity:
                    return False

        return True

    def reserve_ride(self, req: Request) -> None:
        self.reserved.append(req)
        if self.dir == Direction.REST:
            self.dir = Direction.UP if req.start_floor >= self.curr_floor else Direction.DOWN
            

class ElevatorSystem:
    def __init__(self) -> None:
        self.req_queue: deque[Request] = deque() # for requests if all elevators in system are busy and at capacity
        self.elevators: dict[int, Elevator] = {}

    def add_elevator(self, elevator: Elevator) -> None:
        self.elevators[elevator.id] = elevator
        
    def handle_request(self, req: Request) -> None:
        if not self._is_valid_request(req):
            raise ValueError(f"Invalid request: {req}")

        best_dist = float('inf')
        best_elevator = None
        for elevator in self.elevators.values():
            if not elevator.can_reserve_ride(req):
                continue
            dist = abs(req.start_floor - elevator.curr_floor)
            if dist < best_dist:
                best_dist = dist
                best_elevator = elevator

        if best_elevator is None:
            self.req_queue.append(req)
        else:
            best_elevator.reserve_ride(req)

    @staticmethod
    def _is_valid_request(req: Request) -> bool:
        return req.start_floor >= 0 and req.end_floor >= 0 and req.start_floor != req.end_floor

    def tick(self) -> None:
        for elevator in self.elevators.values():
            elevator.tick()

        print("=== New State ===")
        for elevator in self.elevators.values():
            for field, value in vars(elevator).items():
                print(f"{field}: {value}")

    def simulate(self, reqs: list[Request]) -> None:
        reqs = sorted(reqs, key=lambda x: x.ts)
        idx = 0
        ts = 0
        while idx < len(reqs) or self.req_queue or any(e.riders or e.reserved for e in self.elevators.values()):
            for _ in range(len(self.req_queue)):
                req = self.req_queue.popleft()
                self.handle_request(req)

            while idx < len(reqs) and reqs[idx].ts <= ts:
                self.handle_request(reqs[idx])
                idx += 1

            print(f"Time [{ts}, {ts + 1}) has passed")
            self.tick()
            ts += 1


if __name__ == "__main__":
    system = ElevatorSystem()
    e1 = Elevator(5)
    system.add_elevator(e1)
    reqs = [Request(2, 5, 1), Request(3, 7, 2), Request(5, 0, 2)]
    system.simulate(reqs)
