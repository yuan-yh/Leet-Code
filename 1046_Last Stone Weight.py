class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        # Greedy + Max-heap: always pick the most heaviest two and smash
        heap = []
        for s in stones:
            heappush(heap, -s)
        
        while len(heap) > 1:
            t1, t2 = -heappop(heap), -heappop(heap)
            if t1 > t2: heappush(heap, t2-t1)

        return 0 if len(heap) == 0 else -heappop(heap)