class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Binary Search: find the idx i such that nums[i-1] > nums[i]
        l, r = 0, len(nums) - 1     # [start, end]
        while l < r:
            m = (l + r) >> 1
            if m > 0 and nums[m-1] > nums[m]: return nums[m]
            # case: m in the left rotated part: nums[m] > nums[r] -> l = m + 1
            if nums[m] > nums[r]: l = m + 1
            # case: m in the right original part -> r = m - 1
            else: r = m - 1
        return nums[l]