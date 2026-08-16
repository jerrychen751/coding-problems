from collections import defaultdict, deque
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        '''
        [a, b] means b is pre-req to a
        n courses, labeled from 0..n-1
        return array of length n of course sequence, or empty arr if cannot complete sequence

        we need courses that don't show up in prerequisites[i][0] for all i
            if no courses are like this, return empty arr

        DAG; [a, b] [b, a] -> any cycles means return empty arr

        hash map with adjacency lists:
        {0: [1, 2], 1: [3], 2: [3]}

        BFS; take all courses take-able at a particular level before proceeding onward
        Topological sort, Kahn's algorithm

        Maintain an array deg where deg[i] is number of edges pointing towards course i
        If deg[i] == 0, this course is "unlocked" and able to be taken; store these in a queue and process one by one
        When processing a course, decrease deg[j] for all j that i is a pre-req for, add course to sequence result

        if in the end len(sequence) != numCourses, we return empty array
        '''

        prereqs = defaultdict(list) # potentially DAG mapping node to all courses that it helps unlock / points to
        deg = [0] * numCourses
        sequence = []
        queue = deque()
        for course, dep in prerequisites:
            prereqs[dep].append(course)
            deg[course] += 1

        for i in range(numCourses):
            if deg[i] == 0:
                queue.append(i)

        while queue:
            curr = queue.popleft()
            sequence.append(curr)
            for course in prereqs[curr]:
                deg[course] -= 1
                if deg[course] == 0:
                    queue.append(course)

        if len(sequence) == numCourses:
            return sequence

        return []
