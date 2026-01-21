class Solution:
    def trap(self, height: List[int]) -> int:
        if len(height) <= 2: return 0

        l, r, lMax, rMax, res = 1, len(height) - 2, height[0], height[-1], 0

        while l <= r:
            if lMax < rMax:
                lMax = max(lMax, height[l])
                res += lMax - height[l]
                l += 1
            else:
                rMax = max(rMax, height[r])
                res += rMax - height[r]
                r -= 1
        return res