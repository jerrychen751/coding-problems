from collections import deque


class Solution:
    def getMinSwaps(self, num: str, k: int) -> int:
        # To obtain the smallest (k=1) wonderful integer, we start scanning num from the right
        # There is the possibility of obtaining a larger number through digit swaps when the digit to the left
        # is smaller than SOME digit we have already seen

        # To obtain the very next wonderful integer after an integer, we swap with the smallest integer we have already seen
        # which is still greater than the compared digit

        # "5489355142"
        # 2, 4, 1 <- stop here
        # Of {2, 4}, what is the smallest number that can swap with 1, which is still > 1
        # ...2?? <- swap out the digit, and then re-create the suffix in "sorted order" with {4, 1}
        # Can reverse due to invaraint of non-increasing order moving rightward

        # These simulations lead to k-th wonderful number, and now assuming we have that number, find minSwaps
        # For min swaps, move rightward through the number
        # At each location where it doesn't match the final number, bubble the first correct number on the right side to the left
        # performing pairwise swaps at each location
        # Simulate and add the number

        def kth_wonderful_number(num: str, k: int) -> str:
            curr = 0 # tracks number of curr permutation which is greater than num
            num = [c for c in num]
            while curr < k:
                last = num[-1]
                for i in range(len(num) - 2, -1, -1):
                    if num[i] >= last:
                        # only way to keep moving left is if numbers are monotonically increasing from right to left
                        last = num[i]
                        continue

                    # Find the smallest digit to the right which is still greater -> swap + reverse suffix
                    for j in range(len(num) - 1, i, -1):
                        if num[i] < num[j]:
                            num[i], num[j] = num[j], num[i]
                            suffix = num[i + 1:]
                            num = num[:i + 1] + suffix[::-1]
                            break

                    break

                curr += 1

            return "".join(num)

        # Obtain inversion array
        target = kth_wonderful_number(num, k)
        hmap = {}
        for i, c in enumerate(target):
            if c not in hmap:
                hmap[c] = deque([i])
            else:
                hmap[c].append(i)

        inv_arr = []
        for c in num:
            inv_arr.append(hmap[c].popleft())

        # Count inversions
        def count_inversions(arr: list[int]) -> int:
            temp = [0] * len(arr) # temp array to help with merge step
            def _count_sort(lo: int, hi: int) -> int:
                """Sorts arr[lo:hi] and returns contribution to inversion count"""
                if hi - lo <= 1:
                    return 0

                mid = lo + (hi - lo) // 2
                left_inv = _count_sort(lo, mid)
                right_inv = _count_sort(mid, hi)
                merge_inv = _count_merge(lo, mid, hi)
                return left_inv + right_inv + merge_inv

            def _count_merge(lo: int, mid: int, hi: int) -> int:
                """Merges arr[lo:mid] and arr[mid:hi], two sorted portions of arr, and returns inversion count contribution"""
                i = lo
                j = mid
                k = lo

                inv = 0
                while i < mid and j < hi:
                    if arr[i] <= arr[j]:
                        temp[k] = arr[i]
                        i += 1
                    else:
                        temp[k] = arr[j]
                        inv += mid - i
                        j += 1
                    k += 1

                while i < mid:
                    temp[k] = arr[i]
                    i += 1
                    k += 1
                while j < hi:
                    temp[k] = arr[j]
                    j += 1
                    k += 1

                for i in range(lo, hi):
                    arr[i] = temp[i]

                return inv

            return _count_sort(0, len(arr))

        return count_inversions(inv_arr)
