class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r) >> 1

            if nums[m] == target:
                return m
            
            # 1. mid in smaller
            if nums[m] < nums[r]:
                if target < nums[m] or target > nums[r]:
                    r = m - 1
                else:
                    l = m + 1
            # 2. mid in greater
            else:
                if target > nums[m] or target < nums[l]:
                    l = m + 1
                else:
                    r = m - 1

        return l if nums[l] == target else -1