class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # 2-ptr w/ in-place swap
        l = 0
        for r in range(len(nums)):
            if nums[r] != nums[l]:
                l += 1
                nums[l] = nums[r]
        return l + 1