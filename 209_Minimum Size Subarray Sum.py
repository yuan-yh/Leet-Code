class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l, curSum, res = 0, 0, inf

        for r, n in enumerate(nums):
            curSum += n
            while curSum >= target:
                res = min(res, r-l+1)
                curSum -= nums[l]
                l += 1
        return 0 if res == inf else res