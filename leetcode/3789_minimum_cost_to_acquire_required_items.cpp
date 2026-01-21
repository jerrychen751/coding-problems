#include <algorithm>

class Solution {
public:
    long long minimumCost(int cost1, int cost2, int costBoth, int need1, int need2) {
        long long total_cost = 0;

        // Decision 1: whether to use costBoth to fulfill one need completely
        long long common = std::min(need1, need2);
        total_cost += std::min(cost1 + cost2, costBoth) * common;

        // Decision 2: whether to use costBoth to fulfill remaining need fully
        total_cost += std::min(cost1, costBoth) * (need1 - common);
        total_cost += std::min(cost2, costBoth) * (need2 - common);

        return total_cost;
    }
};