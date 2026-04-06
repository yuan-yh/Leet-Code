class Solution:
    def trap(self, height: List[int]) -> int:
        # 2-Pointer: shift towards center
        # the lower boundary determines the trapped amount
        res, l, r, lMax, rMax = 0, 0, len(height) - 1, 0, 0

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