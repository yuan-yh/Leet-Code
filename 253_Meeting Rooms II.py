class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # Heap: when loop a new meeting, pop ended -> push end time -> record max length
        res = 0
        heap = []

        # 1. sort based on the starting time
        intervals.sort(key = lambda x : x[0])

        for start, end in intervals:
            # 2. pop expired meetings
            while heap and heap[0] <= start: heappop(heap)
            # 3. push new end time
            heappush(heap, end)
            # 4. record max rooms
            res = max(res, len(heap))
        return res