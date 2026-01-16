# Reference: https://leetcode.cn/problems/non-overlapping-intervals/solutions/3077218/tan-xin-zheng-ming-pythonjavaccgojsrust-3jx4f/

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # 贪心策略：总是选择最早结束的interval, 因为越早结束->剩余的时间越多->能容纳更多intervals
        # 1. sort
        intervals.sort(key = lambda x : x[1])
        # 2. greedy
        cnt, prevEnd = 0, -inf
        for start, end in intervals:
            # non-overlap
            if start >= prevEnd: prevEnd = end
            # overlap
            else: cnt += 1
        return cnt