class Solution:
    def maxArea(self, height: List[int]) -> int:
        # width: r-l; height: min(h[l], h[r]) -> shift the lower boundary
        res, l, r = 0, 0, len(height) - 1

        while l < r:
            res = max(res, (r-l)*(min(height[l], height[r])))
            if height[l] < height[r]: l += 1
            else: r -= 1
        return res