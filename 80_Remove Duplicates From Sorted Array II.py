class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # two-pointer
        # For 2-appearance at most, since nums is sorted, we can just check adj digit instead of dictionary/hashmap
        slow = 0
        for i in nums:
            if slow < 2 or i != nums[slow - 2]:
                nums[slow] = i
                slow += 1
        return slow