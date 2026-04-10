class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # 1. sort based on start time
        intervals.sort(key = lambda x : x[0])
        # 2. track room based on end time (min-heap)
        room = []
        res = 0

        for start, end in intervals:
            while room and room[0] <= start: heappop(room)
            heappush(room, end)
            res = max(res, len(room))
        return res