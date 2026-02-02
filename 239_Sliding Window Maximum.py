class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # Monotonic stack: record idx of mono-decreasing elements
        res = []
        stack = deque()

        for i, n in enumerate(nums):
            # 1. remove n[q_idx] <= cur element
            while stack and nums[stack[-1]] <= n: stack.pop()
            # 2. append cur idx
            stack.append(i)
            # 3. remove expired idx outside the window
            left = i - k + 1
            # 4. record stack[0]
            if left >= 0:
                while stack[0] < left: stack.popleft()
                res.append(nums[stack[0]])

        return res