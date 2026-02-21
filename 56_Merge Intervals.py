class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        res = []

        # 1. sort based on start time
        intervals.sort(key = lambda x : x[0])

        # 2. merge if curStart <= lastEnd, else attach
        res.append(intervals[0])

        for start, end in intervals[1:]:
            if start <= res[-1][1]: res[-1][1] = max(end, res[-1][1])
            else: res.append([start, end])

        return res