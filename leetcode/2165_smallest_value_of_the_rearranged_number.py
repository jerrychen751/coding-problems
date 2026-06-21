import heapq

class Solution:
    def smallestNumber(self, num: int) -> int:
        # Greedy problem
        # If positive, build min-heap and pop to build smallest number; any zeros popped from min-heap go after first non-zero
        # If negative, build max-heap with digits

        if num == 0:
            return 0

        base = 10
        smallest = 0
        heap = []
        is_neg = num < 0
        num = abs(num)
        while num > 0:
            num, remainder = divmod(num, 10)
            heap.append(remainder)
        if is_neg:
            heap = [-x for x in heap]

        heapq.heapify(heap)
        if not is_neg:
            x = heapq.heappop(heap)
            zero_ct = 0
            while x == 0:
                zero_ct += 1
                x = heapq.heappop(heap)
            smallest = x * (base ** zero_ct)
        while len(heap) > 0:
            smallest *= base
            smallest += heapq.heappop(heap)

        return smallest
