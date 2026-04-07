class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        res = []

        # 1. sort
        intervals.sort(key = lambda x : x[0])
        # 2. merge
        for start, end in intervals:
            if not res or start > res[-1][1]: res.append([start, end])
            else: res[-1][1] = max(end, res[-1][1])

        return res