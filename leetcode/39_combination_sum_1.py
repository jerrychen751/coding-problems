from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        '''
        Recursion to select elements
        Sort candidates array so that we can early exit
        i.e. if sum_path + candidates[idx] > target -> no need to check indices greater than idx
        '''
        res = []
        candidates = sorted(candidates)
        def backtrack(path: list[int], path_sum: int, idx: int) -> None:
            if path_sum > target:
                return
            if path_sum == target:
                res.append(path.copy())
                return

            for i in range(idx, len(candidates)):
                num = candidates[i]
                if path_sum + num > target:
                    break
                path.append(num)
                path_sum += num
                backtrack(path, path_sum, i)
                path.pop()
                path_sum -= num

        backtrack([], 0, 0)
        return res
