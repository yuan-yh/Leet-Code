class KthLargest:
    # min-heap: track top k largest element & top = target
    def __init__(self, k: int, nums: List[int]):
        self.capacity = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > self.capacity: heappop(self.heap)

    def add(self, val: int) -> int:
        heappush(self.heap, val)
        if len(self.heap) > self.capacity: heappop(self.heap)
        return self.heap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)