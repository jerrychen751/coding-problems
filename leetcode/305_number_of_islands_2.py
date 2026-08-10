from typing import List


class Solution1:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        # Given positions, we need to make sure each island has a unique identity
        # When we add a new piece of land, there are a few cases
        # 1. New position is surrounded by water on all 4 dirs -> increase number of islands from before
        # 2. New position has 1 or more land cells adjacent to it -> all adjacent islands need to be flood filled
        # of 4 adj dirs, count how many distinct identities of land there are; number of islands changes by (1 - distinct)

        # To avoid repeatedly flood-filling large regions, maintain a mapping that maps identity: size for each unique island
        # And pick the identity with the largest size (when scenario 2) to flood fill with

        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        def flood_fill(grid: list[list[int]], fill_id: int, i: int, j: int) -> None:
            if not in_bounds(i, j):
                return
            if grid[i][j] == 0 or grid[i][j] == fill_id:
                return

            grid[i][j] = fill_id
            for di, dj in dirs:
                flood_fill(grid, fill_id, i + di, j + dj)


        grid = [[0 for _ in range(n)] for _ in range(m)]
        island_sizes = {}
        num_islands = []
        island_id = 1 # start at 1, increasing-only number representing unique identity of an island
        for i, j in positions:
            # Edge case: repeated positions
            if grid[i][j] != 0:
                num_islands.append(num_islands[-1])
                continue

            neighbors = set()
            for di, dj in dirs:
                new_i, new_j = i + di, j + dj
                if in_bounds(new_i, new_j) and grid[new_i][new_j] != 0 and grid[new_i][new_j] not in neighbors:
                    neighbors.add(grid[new_i][new_j])

            # Update number of islands
            if not num_islands:
                # Base case; first position
                num_islands.append(1)
            else:
                num_islands.append(num_islands[-1] + 1 - len(neighbors))

            # Update island sizes and state
            if len(neighbors) == 0:
                # New island formed
                grid[i][j] = island_id
                island_sizes[island_id] = 1
                island_id += 1
            else:
                # Flood fill to update state since there are adjacent land cells
                # Also update sizes after determining what to fill as
                largest_island = max(neighbors, key=lambda neighbor: island_sizes[neighbor])

                for neighbor in neighbors:
                    if neighbor != largest_island:
                        island_sizes[largest_island] += island_sizes[neighbor]
                        del island_sizes[neighbor]

                # Now we know which is largest so which to fill with
                grid[i][j] = island_id
                flood_fill(grid, largest_island, i, j)
                island_sizes[largest_island] += 1 # add curr land position as well

        return num_islands


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[tuple[int, int], tuple[int, int]] = {} # maps one (i, j) cell to its ultimate parent identity
        # cells with the same ultimate parent are part of same connected component
        self.size: dict[tuple[int, int], int] = {}

    def add(self, cell: tuple[int, int]) -> bool:
        if cell in self.parent:
            return False

        self.parent[cell] = cell
        self.size[cell] = 1
        return True

    def find(self, cell: tuple[int, int]) -> tuple[int, int]:
        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])

        return self.parent[cell]

    def union(self, first: tuple[int, int], second: tuple[int, int]) -> bool:
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            return False

        if self.size[first_root] < self.size[second_root]:
            first_root, second_root = second_root, first_root

        # first_root guaranteed to be larger size than second_root
        self.parent[second_root] = first_root
        self.size[first_root] += self.size[second_root]
        return True


class Solution2:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        union_find = UnionFind()
        num_islands = []
        island_ct = 0

        def in_bounds(cell: tuple[int, int]) -> bool:
            i, j = cell
            return i >= 0 and i < m and j >= 0 and j < n

        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for i, j in positions:
            cell = (i, j)
            if not union_find.add(cell):
                # cell already exists in there; duplicate positions
                num_islands.append(island_ct)
                continue

            island_ct += 1
            for di, dj in dirs:
                new_i, new_j = i + di, j + dj
                neighbor = (new_i, new_j)
                if in_bounds(neighbor) and neighbor in union_find.parent and union_find.union(cell, neighbor):
                    # in bounds, neighbor is also land, not part of same component
                    island_ct -= 1

            num_islands.append(island_ct)

        return num_islands
