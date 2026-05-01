from collections import deque


class Solution1:
    def nthUglyNumber(self, n: int) -> int:
        # Looks like we just have to compute up to n
        # 1, 2, 3, 2*2, 5, 2*3, 2*2*2, 2*5, 2*2*3, 3*5, 2*2*2*2, 2*2*5
        # [1]

        # Start with base case of first ugly number being 1
        # Set up a queue of ugly numbers. Push to queue when a new ugly number is formed. Pop from left when an ugly number
        # has been multiplied with 5 (multiplying 2, 3, 5 in order from smallest to largest)

        # Idea 1: Have a queue of ugly numbers.
        # When we have a new ugly number, push to back of queue
        # While we still need to generate ugly numbers, start multiplying 2/3/5 for each number in the queue.
        # If queue[0] * 2/3/5 <= queue[-1], then we need to increase factor we're multiplying by. For example, 2 -> 3 -> 5.
        # If queue[0] * 5 <= queue[-1], we pop front of queue.
        # We have a tracker for ugly_num and we pick the min. For example, if queue[1] * 2 < queue[0] * 3, we pick queue[1] * 2 as new ugly num
        # We iterate through the queue until queue[i] * 2 > ugly_num
        # Then no starting ugly number from i...end will work for a better ugly number

        queue = deque([1])
        factors = [2, 3, 5]
        ct = 1 # counter for ugly numbers
        while ct < n and queue:
            # popleft for a used-up ugly number
            while queue and queue[0] * factors[-1] <= queue[-1]:
                queue.popleft()

            best = float('inf')
            for num in queue:
                # early exit
                if num * factors[0] >= best:
                    break

                # obtain next smallest ugly number
                for f in factors:
                    candidate = num * f
                    if candidate <= queue[-1]:
                        continue
                    best = min(candidate, best)
                    break

            queue.append(best)
            ct += 1

        return queue[-1]


class Solution2:
    def nthUglyNumber(self, n: int) -> int:
        # Idea 2: express numbers as triplets of powers of 2/3/5 (1 would be 0,0,0; 2 would be 1,0,0)
        # Every new ugly number must be 2u, 3u, or 5u for some smaller ugly u
        # all u = 2^a * 3^b * 5^c
        # for any particular new ugly number, it would be 2*(2^(a-1) * 3^b + 5^c) or 3... or 5...

        # There are three streams: 2U, 3U, 5U where U is the set of ugly numbers
        # Final result is the merging of these 3 sorted streams
        # ugly_nums serves as both a cache of previous ugly numbers, used to compute the next stream value ad hoc
        # but also as the final result

        ugly_nums = [0] * n
        ugly_nums[0] = 1
        p1 = p2 = p3 = 0 # how many times a particular stream has contributed a value (indexing into stream)
        for i in range(1, n):
            # Determine candidates
            c1 = ugly_nums[p1] * 2
            c2 = ugly_nums[p2] * 3
            c3 = ugly_nums[p3] * 5
            new = min(c1, c2, c3)
            ugly_nums[i] = new
            if c1 == new:
                p1 += 1
            if c2 == new:
                p2 += 1
            if c3 == new:
                p3 += 1


        return ugly_nums[-1]
