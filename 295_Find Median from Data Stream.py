class MedianFinder:
    # Use left (max-heap) / right (min-heap), put median in left when odd total
    def __init__(self):
        self.left = []      # max-heap
        self.right = []     # min-heap

    def addNum(self, num: int) -> None:
        if len(self.left) == len(self.right):
            # push into right -> min into left
            heappush(self.left, -heappushpop(self.right, num))
        else:
            # push into left -> max into right
            heappush(self.right, -heappushpop(self.left, -num))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right): return -self.left[0]
        return (self.right[0] - self.left[0]) / 2


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()