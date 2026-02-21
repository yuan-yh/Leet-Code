# class Solution:
#     def firstMissingPositive(self, nums: List[int]) -> int:
#         nums = set(nums)
#         for i in range(1, len(nums)+1):
#             if i not in nums: return i
#         return len(nums)+1

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        """ TC O(n) & SC O(1) -> likely two-pointer
        res in range [1, len(nums) + 1], so we only care about this range
        Then swap nums[i] onto idx nums[i]-1 and later check
        """
        # 1. swap
        for i in range(len(nums)):
            # A. 0 < nums[i] <= len(nums)
            # B. if i+1 != nums[i], then need to swap onto the idx (nums[i]-1)
            # C. prevent loop: check if the target idx has nums[i] already
            while (0 < nums[i] <= len(nums)) and (nums[i] != i+1) and (nums[nums[i]-1] != nums[i]):
                tmp = nums[nums[i] - 1]
                nums[nums[i] - 1] = nums[i]
                nums[i] = tmp
        
        # 2. check
        for i, n in enumerate(nums):
            if n != i + 1: return i+1
        
        return len(nums)+1