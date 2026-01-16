class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:      
        res = []
        l, r, p, length = newInterval[0], newInterval[1], 0, len(intervals)
        
        # 1. record non-overlapping left: b < l
        while p < length and intervals[p][1] < l: 
            res.append([intervals[p][0], intervals[p][1]])
            p += 1
        # 2. record overlapping & merge: a <= r
        res.append([l, r])
        while p < length and intervals[p][0] <= r:
            res[-1][0], res[-1][1] = min(res[-1][0], intervals[p][0]), max(res[-1][1], intervals[p][1])
            p += 1
        # 3. record non-overlapping right: a > r
        while p < length: 
            res.append([intervals[p][0], intervals[p][1]])
            p += 1
        return res