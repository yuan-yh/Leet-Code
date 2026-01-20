class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # two-pointer
        slow = 0
        record = set()

        for i in nums:
            if i not in record:
                nums[slow] = i
                slow += 1
                record.add(i)
        return slow