class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Key Insight: sort based on the end time -> before inter[i]: processed; after inter[i]: overlap (cnt) or future intervals
        # 贪心策略：总是选择最早结束的interval, 因为越早结束->剩余的时间越多->能容纳更多intervals
        # 1. sort based on x[1]
        intervals.sort(key = lambda x : x[1])
        
        # 2. loop
        cnt, prevEnd = 0, -inf
        for start, end in intervals:
            # case 1: overlap: start < prevEnd: cnt ++
            if start < prevEnd: cnt += 1
            # case 2: start >= prevEnd -> update prevEnd
            else: prevEnd = end
        return cnt