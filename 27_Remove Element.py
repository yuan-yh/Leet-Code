class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # two-pointer
        slow = 0
        for i in nums:
            if i != val:
                nums[slow] = i
                slow += 1
        return slow