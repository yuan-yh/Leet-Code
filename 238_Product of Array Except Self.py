class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = []

        pre = post = 1
        # 1. build pre-product
        for n in nums:
            res.append(pre)
            pre *= n
        # 2. build post-product
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= post
            post *= nums[i]
        
        return res