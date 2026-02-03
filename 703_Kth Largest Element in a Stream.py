class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        # Min-heap: track k largest element, heap top is the kth largest
        self.capacity = k
        self.minHeap = nums
        heapq.heapify(self.minHeap)

    def add(self, val: int) -> int:
        heappush(self.minHeap, val)
        while len(self.minHeap) > self.capacity: heappop(self.minHeap)
        return self.minHeap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)