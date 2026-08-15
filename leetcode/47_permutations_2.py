from typing import List


class Solution1:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        '''
        permutation is array of ints, return list of unique permutations
        duplicates in nums

        1, 2, 2

        1 2 2
        1 2 2
        2 1 2
        2 2 1
        2 1 2
        2 2 1

        set of indices used
        set of permutations generated
        n*n! time and space

        ordering becomes important to avoid duplicate permutations
        used indices set
        within the loop in recursive function, we want to skip forward indices to try as start of next branch until we find a different number

        '''

        res = []
        nums.sort()
        def backtrack(path: list[int], used: set[int]) -> None:
            if len(used) == len(nums):
                res.append(path.copy())
                return

            prev = None
            for i in range(len(nums)):
                if i in used:
                    continue
                if nums[i] == prev:
                    continue

                prev = nums[i]
                path.append(nums[i])
                used.add(i)
                backtrack(path, used)
                used.remove(i)
                path.pop()

        backtrack([], set())
        return res


class Solution2:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        '''
        permutation is array of ints, return list of unique permutations
        duplicates in nums

        1, 2, 2

        1 2 2
        1 2 2
        2 1 2
        2 2 1
        2 1 2
        2 2 1

        set of indices used
        set of permutations generated
        n*n! time and space

        ordering becomes important to avoid duplicate permutations
        used indices set
        within the loop in recursive function, we want to skip forward indices to try as start of next branch until we find a different number

        '''

        res = []
        def backtrack(path: list[int], used: set[int]) -> None:
            if len(used) == len(nums):
                res.append(path.copy())
                return

            used_roots = set() # root is start of branch, i.e., the value that we append onto path in this frame
            for i in range(len(nums)):
                if i in used:
                    continue
                if nums[i] in used_roots:
                    continue

                prev = nums[i]
                path.append(nums[i])
                used.add(i)
                backtrack(path, used)
                used.remove(i)
                path.pop()

                used_roots.add(nums[i])

        backtrack([], set())
        return res
