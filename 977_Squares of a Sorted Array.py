class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        # 2-Pointer towards center
        res = [0] * len(nums)
        l, r, p = 0, len(nums) - 1, len(nums) - 1

        while p >= 0:
            if abs(nums[l]) > abs(nums[r]):
                res[p] = nums[l] * nums[l]
                l += 1
            else:
                res[p] = nums[r] * nums[r]
                r -= 1
            p -= 1
        return res