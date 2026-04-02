class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # Binary Search in [left, right)
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) >> 1
            if nums[mid] == target: return mid
            elif nums[mid] < target: left = mid + 1
            else: right = mid
        return left