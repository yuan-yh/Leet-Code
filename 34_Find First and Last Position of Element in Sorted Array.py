class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        左中点会偏左: (l + r) >> 1
        右中点会偏右: (l + r + 1) >> 1
        当 l 和 r 相邻时，必须保证更新还会动, so r=m w/ 左中点 and l=m w/右中点
        """
        def searchLeft(l, r) -> int:    # [l, r]
            while l < r:
                m = (l + r) >> 1
                if nums[m] >= target: r = m
                else: l = m + 1
            return -1 if nums[l] != target else l
        
        def searchRight(l, r) -> int:    # [l, r]
            while l < r:
                m = (l + r + 1) >> 1
                if nums[m] <= target: l = m
                else: r = m - 1
            return -1 if nums[l] != target else l

        left = -1 if len(nums) == 0 else searchLeft(0, len(nums) - 1)
        if left == -1: return [-1, -1]
        right = searchRight(left, len(nums) - 1)
        return [left, right]