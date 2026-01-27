class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        """
        DAG: start from idx 0, point to nums[0] - the next idx is the val of the cur idx in the array
        Similar to LC 142
        """
        head = fast = slow = 0      # init as 0 as nums[i] in [1, n]
        # 1. let fast / slow meet in the cycle
        while fast == 0 or slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]
        # 2. find the cycle start
        while head == 0 or slow != head:
            slow = nums[slow]
            head = nums[head]
        return head