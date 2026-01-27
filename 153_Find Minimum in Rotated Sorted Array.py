class Solution:
    def findMin(self, nums: List[int]) -> int:
        # short-cut
        if nums[0] < nums[-1]: return nums[0]

        # Binary Search for i such that nums[i] < nums[i-1] in [l, r]
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) >> 1
            # case: in the left rotated part: nums[m] > nums[r] -> l = m+1
            if nums[m] > nums[r]: l = m + 1
            # case: in the right original part: nums[m] <= nums[r] -> r = m
            else: r = m
        return nums[l]