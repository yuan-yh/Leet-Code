class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # [greater, smaller]
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) >> 1

            if nums[m] == target: return m

            # Case: in greater range
            # nums[m] > target:
            #   nums[l] <= target: [l, m-1]
            #   nums[l] > target: [m+1, r]
            # nums[m] < target: [m+1, r]
            if nums[m] > nums[r]:
                if nums[l] <= target < nums[m]: r = m - 1
                else: l = m + 1
            # Case: in smaller range
            # nums[m] > target: [l, m-1]
            # nums[m] < target: 
            #   nums[r] < target: [l, m-1]
            #   nums[r] >= target: [m+1, r]
            else:
                if nums[m] < target <= nums[r]: l = m + 1
                else: r = m - 1
        
        return l if nums[l] == target else -1