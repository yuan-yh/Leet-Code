class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        def search(start, end, goal) -> int:
            # [start, end]
            while start <= end:
                m = (start + end) >> 1
                if nums[m] == goal: return m
                elif nums[m] < goal: start = m + 1
                else: end = m - 1
            return -1

        # Binary search in nums[i+1:]
        for i, n in enumerate(nums):
            res = search(i+1, len(nums)-1, target-n)
            if res != -1: return [i+1, res+1]
        return [-1, -1]