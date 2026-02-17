from typing import List

class Solution:
    def maximumTastiness(self, price: List[int], k: int) -> int:
        # price is array of positive ints, where price[i] is price of i-th candy
        # the store sells baskets of k different candies; tastiness of candy basket is the min absolute diff
        # between the prices of any two candies in the basket

        # Return max tastiness of a candy basket

        # Assume k <= len(price)? yes
        # Can k < 2? no
        # Assume that each candy is distinct? Like len(price) = num candies?
        # How do we know if a candy is distinct? If it has a different price?

        # Smallest absolute difference, means that we want the candies picked to have prices with differences
        # Which are as similar as possible

        # Approach
        # If k = 2, we can take the elements at either end and then return that
        # Otherwise, sort the array
        # We have a range of possible values for tastiness, from 0 to max(price) - min(price)
        # Try a binary search approach, where we pick out a specific tastiness value and test whether it's achievable

        # To know if it's achievable, we can move across the sorted array and see the difference between elements
        # Start from the beginning, we want to pick the first candy that gives us a diff >= tastiness
        # That will guarantee that we can pick out as many candies as possible in a basket, since we want len(basket) >= k

        if k == 2:
            return max(price) - min(price)

        price.sort()
        max_tastiness = price[-1] - price[0] # iterate through candidates to determine whether it's achievable
        min_tastiness = 0
        basket_size = 0
        best = 0
        while min_tastiness <= max_tastiness:
            target = min_tastiness + (max_tastiness - min_tastiness) // 2
            if self.tastinessAchievable(target, k, price):
                best = max(best, target)
                min_tastiness = target + 1
            else:
                max_tastiness = target - 1
        
        return best
    
    def tastinessAchievable(self, target: int, k: int, prices: list[int]) -> bool:
        prev = prices[0] # compare difference between current and prev
        k -= 1
        for i in range(1, len(prices)):
            if prices[i] - prev >= target:
                prev = prices[i]
                k -= 1
            
        return k <= 0
        