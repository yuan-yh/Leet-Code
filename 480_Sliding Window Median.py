class LazyHeap:
    def __init__(self):
        self.heap = []
        self.size = 0
        self.removeCnt = defaultdict(int)
    
    def remove(self, n):
        self.size -= 1
        self.removeCnt[n] += 1
    
    def apply_remove(self):
        # perform DEL when the heap top should be removed
        while self.heap and self.removeCnt[self.heap[0]] > 0:
            self.removeCnt[self.heap[0]] -= 1
            heappop(self.heap)
    
    def peek(self) -> int:
        self.apply_remove()
        return self.heap[0]
    
    def pop(self) -> int:
        self.apply_remove()
        self.size -= 1
        return heappop(self.heap)

    def push(self, n) -> int:
        heappush(self.heap, n)
        self.size += 1

    def pushpop(self, n) -> int:
        self.push(n)
        return self.pop()


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        # left/right array to track digits in the window
        # Lazy deletion: when left window, use a hashmap to track del_cnt of digits
        left = LazyHeap()       # max-heap
        right = LazyHeap()      # min-heap
        res = []

        # 1. maintain left/right median
        for i, n in enumerate(nums):
            if left.size == right.size: # push into right -> min into left
                left.push(-right.pushpop(n))
            else:                       # push into left -> max into right
                right.push(-left.pushpop(-n))
        
            wstart = i - k + 1
            if wstart < 0: continue

            # 2. calculate median & record
            # case: odd vs even window size
            if k % 2 == 0: res.append((right.peek() - left.peek()) / 2)
            else: res.append(-left.peek())

            # 3. update the window start by discarding the expire element
            expire = nums[wstart]
            # case 1: expire in left -> remove & balance heap size
            if expire <= -left.peek():
                left.remove(-expire)
                if left.size < right.size:
                    left.push(-right.pop())
            # case 2: expire in right
            else:
                right.remove(expire)
                if left.size > right.size + 1:
                    right.push(-left.pop())
    
        return res