class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # 1. sort based on the start time
        intervals.sort(key = lambda x : x[0])
        # 2. record
        res = []

        for start, end in intervals:
            # new start: no-merge or empty res
            if len(res) == 0 or start > res[-1][1]: res.append([start, end])
            # merge
            else: res[-1][1] = max(res[-1][1], end)
        return res