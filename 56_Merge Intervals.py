class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # 1. sort
        intervals.sort(key = lambda x : x[0])
        # 2. merge
        res = [ [intervals[0][0], intervals[0][1]] ]

        for a, b in intervals[1:]:
            if a <= res[-1][1]: res[-1][1] = max(res[-1][1], b)
            else: res.append([a, b])
        return res