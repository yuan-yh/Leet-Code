class Solution:
    # Method: Deque based on 'idx'
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque() # DESC Order of digits but record in idx

        for i, n in enumerate(nums):
            while q and n >= nums[q[-1]]: q.pop()
            q.append(i)

            start = i - k + 1
            if start >= 0:
                res.append(nums[q[0]])
                if q[0] == start: q.popleft()
        return res

    # # Method: Max-Heap based on (digit, index)
    # def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
    #     # Max-heap to track the max value within the current valid window
    #     res, max_heap = [], []

    #     # 1. init
    #     for i in range(k-1): heappush(max_heap, (-nums[i], i))

    #     # 2. loop
    #     expire = -1
    #     for i in range(k-1, len(nums)):
    #         # expire
    #         while max_heap and max_heap[0][1] <= expire: 
    #             heappop(max_heap)
    #         # add cur digit
    #         heappush(max_heap, (-nums[i], i))
    #         # find the max
    #         res.append(-max_heap[0][0])
    #         expire += 1

    #     return res