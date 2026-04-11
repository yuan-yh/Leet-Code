class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1: return 1
        # 1. init: location_0 and location_1
        prev = cur = 1
        # 2. update
        for _ in range(2, n+1):
            prev, cur = cur, prev + cur
        return cur