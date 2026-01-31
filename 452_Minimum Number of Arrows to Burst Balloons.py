class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        # Greedy + Overlapping
        # 1. sort based on the intervals-end, which is where we burst the balloon
        points.sort(key = lambda x : x[1])
        # 2. loop
        res = 1
        burst = points[0][1]
        for start, end in points:
            # shoot a new one when start > burst
            if start > burst:
                burst = end
                res += 1

        return res