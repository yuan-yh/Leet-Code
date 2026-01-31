class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Given the sorted intervals in ASC, split into 3 parts: non-overlap before, merge, non-overlap-after
        res = []
        i, l = 0, len(intervals)

        # 1. non-overlap before: end < nstart
        while i < l and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1
        # 2. merge: nend >= start
        while i < l and newInterval[1] >= intervals[i][0]:
            newInterval[0], newInterval[1] = min(newInterval[0], intervals[i][0]), max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)
        # 3. non-overlap-after: nend < start
        while i < l:
            res.append(intervals[i])
            i += 1

        return res