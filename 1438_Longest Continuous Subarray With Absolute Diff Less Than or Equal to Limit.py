class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # Monotonic Stack: Similar to LC239, track the edge value in [idx : r]
        minq, maxq = deque(), deque()
        res = l = 0

        for r in range(len(nums)):
            # 1. expire prev larger values
            while minq and nums[minq[-1]] > nums[r]: minq.pop()
            # 2. expire prev smaller values
            while maxq and nums[maxq[-1]] < nums[r]: maxq.pop()
            # 3. append extreme value starting from the cur window
            minq.append(r)
            maxq.append(r)
            # 4. shrink if invalid
            while abs(nums[maxq[0]] - nums[minq[0]]) > limit:
                l += 1
                if minq[0] < l: minq.popleft()
                if maxq[0] < l: maxq.popleft()
            # 5. update record
            res = max(res, r - l + 1)
        return res