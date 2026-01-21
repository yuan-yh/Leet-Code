class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        length, left, right = len(nums), nums[0], nums[-1]
        res = [1] * length

        # 1. calculate the left-side product of nums[i]
        for i in range(1, length):
            res[i] *= left
            left *= nums[i]
        # 2. calculate the right-side product of nums[i]
        for i in range(length-2, -1, -1):
            res[i] *= right
            right *= nums[i]

        return res