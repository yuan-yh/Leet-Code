class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # For each nums[i], either multiply w/ prev or restart from itself
        # Maintain maxp & minp that ended w/ nums[i]
        res = minp = maxp = nums[0]
        for i in nums[1:]:
            maxp, minp = max(i*maxp, i*minp, i), min(i*maxp, i*minp, i)
            res = max(res, maxp)
        return res