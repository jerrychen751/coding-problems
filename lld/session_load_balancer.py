'''
Session Load Balancer

A cluster has a fixed set of servers, and each server holds user sessions. Design a
ServerManager that assigns every new session to a server and keeps the session counts
balanced across the servers.

Implement the ServerManager class:

- ServerManager(servers: list[str]) creates the manager with the given server ids.
  Every server starts with no sessions.
- add_session(session_id) assigns the session to a server that holds the fewest
  sessions. Raises ValueError if the session already exists.
- remove_session(session_id) ends the session and frees its place on its server.
  Raises ValueError if the session does not exist.
- get_sessions() returns a map from each active session id to the id of its server.

After every call, the session counts of any two servers differ by at most 1. A removal
can break this rule. When it does, one session moves from a server with the most
sessions to the server that lost one.

Example (a tie may go to any of the least loaded servers, so this is one valid run):

    manager = ServerManager(["s1", "s2", "s3"])
    manager.add_session("a")  # a -> s1, loads s1=1 s2=0 s3=0
    manager.add_session("b")  # b -> s2, loads s1=1 s2=1 s3=0
    manager.add_session("c")  # c -> s3, loads s1=1 s2=1 s3=1
    manager.add_session("d")  # d -> s1, loads s1=2 s2=1 s3=1
    manager.remove_session("b")  # s2 drops to 0, so a or d moves from s1 to s2: loads s1=1 s2=1 s3=1
    manager.get_sessions()  # {"a": "s2", "c": "s3", "d": "s1"} if a moved
    manager.add_session("c")  # raises ValueError, c already exists

Constraints:

- servers holds at least one id, and the ids are unique.
- The servers never change after construction.
- A session id is a string that names at most one active session.

Follow-up: can add_session and remove_session each run in O(1) time?
'''

# servers is a string array

class ServerManager:
    def __init__(self, servers: list[str]) -> None:
        self.session_to_server = {} # session id -> server id

        self.server_loads: dict[int, set[str]] = {} # maps int (session ct) to set of server ids
        self.server_loads[0] = set()
        for server in servers:
            self.server_loads[0].add(server)


    def add_session(self, session_id) -> None:
        if session_id in self.session_to_server:
            raise ValueError("Session already exists")

        # Determine which "bucket" of servers to add session to
        loads = list(self.server_loads.keys()) # len 1 or 2
        load = min(loads)

        # Pick a specific server from smaller "bucket", remove it, and add to
        # incremented "bucket"
        # If bucket becomes empty remove that bucket
        server_set = self.server_loads[load]
        server_id = server_set.pop()
        if len(server_set) == 0:
            del self.server_loads[load]

        # Add new server to increment loaded count
        if load + 1 in self.server_loads:
            self.server_loads[load + 1].add(server_id)
        else:
            self.server_loads[load + 1] = set([server_id])

        # Maintain session to server mapping
        self.session_to_server[session_id] = server_id

    def remove_session(self, session_id: str) -> None:
        if session_id not in self.session_to_server:
            raise ValueError("Session does not exist")

        # Get server w/ session_id
        # What bucket is server in? Iterate over self.server_loads check for server in set
        server_id = self.session_to_server[session_id]
        server_bucket = 0
        for bucket in self.server_loads.keys():
            if session_id in self.server_loads[bucket]:
                server_bucket = bucket
                self.server_loads[bucket].remove(server_id)
                break

        # Remove server from that bucket, place in decremented bucket
        if server_bucket - 1 in self.server_loads:
            self.server_loads[server_bucket - 1].add(server_id)
        else:
            self.server_loads[server_bucket - 1] = set([server_id])

        # Check if we have 3 keys; if we have 1 or 2 we're done
        # Take random set from largest bucket, take decremented bucket, move it all to the center bucket
        # Delete empty buckets if needed
        if len(self.server_loads) == 3:
            # server_bucket +/- 1
            smallest_bucket, middle_bucket, largest_bucket = sorted(self.server_loads.keys())

            larger_server = self.server_loads[largest_bucket].pop()
            if len(self.server_loads[largest_bucket]) == 0:
                del self.server_loads[largest_bucket]
            smaller_server = self.server_loads[smallest_bucket].pop()
            del self.server_loads[smallest_bucket]

            self.server_loads[middle_bucket].add(larger_server)
            self.server_loads[middle_bucket].add(smaller_server)

        del self.session_to_server[session_id]

    def get_sessions(self):
        return self.session_to_server


# track an index i, every server less than index i has 1 more session id, than every index >= i.
# index 2:
server = ServerManager(["s1", "s2", "s3"])

for i in range(10):
    server.add_session(f"session_{i}")

from pprint import pprint
pprint(server.get_sessions())

server.remove_session("session_0")
server.remove_session("session_3")

print("After:")
pprint(server.get_sessions())
