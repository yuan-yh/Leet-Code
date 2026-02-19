class Solution:
    def trap(self, height: List[int]) -> int:
        # 2-Pointer: shift towards center
        res, l, r, lMax, rMax = 0, 0, len(height) - 1, height[0], height[-1]

        while l < r:
            lMax = max(lMax, height[l])
            rMax = max(rMax, height[r])
            # the lower boundary determines the trapped amount
            if lMax < rMax:
                res += lMax - height[l]
                l += 1
            else:
                res += rMax - height[r]
                r -= 1
        return res