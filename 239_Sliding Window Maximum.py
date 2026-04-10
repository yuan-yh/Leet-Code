class Solution:
    # Method: Monotonic Stack
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        maxq = deque()  # append max_val_idx within the range

        for i, n in enumerate(nums):
            # 1. expire prev smaller element
            while maxq and nums[maxq[-1]] < n: maxq.pop()
            # 2. append cur element
            maxq.append(i)
            # 3. shrink if invalid
            start = i - k + 1
            if start >= 0:
                if maxq[0] < start: maxq.popleft()
                # 4. update record
                res.append(nums[maxq[0]])
        
        return res