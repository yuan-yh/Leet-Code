class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        # essentially same as LC56?
        if len(intervals) <= 1: return True
        # 1. sort
        intervals.sort(key = lambda x : x[0])
        # 2. check for overlapping
        end = intervals[0][1]
        for a, b in intervals[1:]:
            if a < end: return False
            end = b
        return True