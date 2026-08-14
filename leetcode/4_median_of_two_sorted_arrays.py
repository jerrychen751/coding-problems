from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # nums1, nums2 are sorted, size m, n respectively
        # median: if m+n is odd, we pick center element, otherwise we pick average of two center elements
        # if we imagine nums as merged sorted array, then median would be nums[mid] if m+n is odd, otherwise 
        # (nums[mid] + nums[mid - 1]) // 2 where mid = (m + n) // 2

        # Naive method:
        # Iterate through nums1 and nums2 in order, form nums which is also sorted, append to nums the smaller for nums1 and nums2
        # Return idx calculation as above
        # O(n + m) time, O(n+m) space

        # Perform binary search to achieve log time
        # A = 1, 2, 3, 4, 5, 6, 7, 8
        # B = 1, 2, 3, 4

        # Let B always be shorter array
        # We partition B in half, so let L2=1, 2 and R2=3, 4
        # len(A+B) = 12, so target = 6
        # We guess that len(L1)=4, so L1=1, 2, 3, 4 and R1=5, 6, 7, 8

        # Compare L1[-1] <= R2[0] and L2[-1] <= R1[0]
        # If both are yes, then we've found proper partition
        # If len(A+B) is even, return max(L1+L2) + min(R1+R2) divide by 2, otherwise return min(R1+R2)
        # If L1[-1] > R2[0], then L1 is too large and R1 can be cut out w/ binary search
        # If L2[-1] > R1[0], then L2 is too large and R2 can be cut out w/ binary search (target not in there)
        # No way for both to be larger than first element in right partition due to sorted nature

        A = nums1
        B = nums2
        if len(A) < len(B):
            A, B = B, A
        # B is always shorter than A
        total = len(A) + len(B)
        target = total // 2

        lo, hi = 0, len(B) # binary search on B
        while lo <= hi:
            i = (lo + hi) // 2 # number of elements in left partition of B
            j = target - i # number of elements in L1

            # Determine comparison vals
            B_left = B[i - 1] if i - 1 >= 0 else float('-inf') # rightmost element in left partition of B
            B_right = B[i] if i < len(B) else float('inf') # leftmost element in right partition of B
            A_left = A[j - 1] if j - 1 >= 0 else float('-inf')
            A_right = A[j] if j < len(A) else float('inf')

            if A_left <= B_right and B_left <= A_right:
                # valid partition
                if total % 2 == 0:
                    return (max(A_left, B_left) + min(A_right, B_right)) / 2
                else:
                    return min(A_right, B_right)
            elif A_left > B_right:
                # L1 is too large
                # We control partition size of B, so we expand L2 for L1 to shrink
                # i ultimately increases
                lo = i + 1
            elif B_left > A_right:
                # L2 is too large
                # Shrink L2 -> i decreases
                hi = i - 1
            # No possible case for both due to sortedness
        
