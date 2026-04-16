class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = []
        lp = rp = 1
        # 1. build left-side product
        for n in nums:
            res.append(lp)
            lp *= n
        # 2. build right-side product
        for i in range(len(nums)-1, -1, -1):
            res[i] *= rp
            rp *= nums[i]
        return res