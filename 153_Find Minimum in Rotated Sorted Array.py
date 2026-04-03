class Solution:
    def findMin(self, nums: List[int]) -> int:
        # [greater, smaller]
        l, r = 0, len(nums) - 1

        while l < r:
            # 左中点会偏左, 保证r=m时更新还会动 (r=m w/ 左中点 and l=m w/右中点)
            m = (l + r) >> 1
            # case: in the greater area -> [m+1, r]
            if nums[m] > nums[r]: l = m + 1
            # case: in the smaller area -> [l, m]
            else: r = m
        
        return nums[l]