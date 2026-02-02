class MedianFinder:
    def __init__(self):
        self.left = []      # max-heap (+median if odd total)
        self.right = []     # min-heap

    def addNum(self, num: int) -> None:
        if len(self.left) == len(self.right):
            # push to right -> min add into left
            heappush(self.left, -heappushpop(self.right, num))
        else:
            # push to left -> max add into right
            heappush(self.right, -heappushpop(self.left, -num))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right): return -self.left[0]
        return (self.right[0] - self.left[0]) / 2
        


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()