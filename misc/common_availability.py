# Common availability for all people
# Given each person's availability intervals, return whether there is a time interval when everyone is available.
# Each person's intervals are non-overlapping and may be unsorted. Endpoints are exclusive, so touching intervals do not overlap.
# With k people and n intervals per person, there are N = nk intervals: O(N log N) time and O(N) extra space.

def is_overlapping_availability(availabilities: dict[str, list[list[int]]]) -> bool:
    starts = []
    ends = []
    for avails in availabilities.values():
        for entry in avails:
            starts.append(entry[0])
            ends.append(entry[1])
    starts.sort()
    ends.sort()

    i, j = 0, 0 # i indexes starts, j indexes ends
    n = len(starts)
    people = 0
    target = len(availabilities)
    while i < n and j < n:
        start = starts[i]
        end = ends[j]
        if start < end:
            people += 1
            if people == target:
                return True
            i += 1
        else:
            people -= 1
            j += 1

    return False

avails = {
    "Greg": [[0, 15], [20, 25]],
    "Fiona": [[30, 35], [5, 15]],
    "Maria": [[0, 5], [10, 20], [25, 30]]
}


avails = {
    "Greg": [[0, 10], [20, 25]],
    "Fiona": [[30, 35], [5, 15]]
}

avails = {
    "Greg": [[20, 25], [0, 10]],
    "Fiona": [[10, 20], [25, 30]]
}

print(is_overlapping_availability(avails))
