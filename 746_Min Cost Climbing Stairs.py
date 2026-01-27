class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        curs = nexts = 0
        for c in cost:
            # cost for the next 2 steps from here = curs + c
            # cost for the next step = min(nexts, curs + c)
            # cost for the next next step = curs + c
            curs, nexts = min(nexts, curs + c), curs + c
        return curs