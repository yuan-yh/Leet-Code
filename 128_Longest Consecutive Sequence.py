class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # Find the min of a consecutive array then expand rightwards
        res = 0

        # 1. hashset for quickly locate
        nums = set(nums)

        for n in nums:
            # 2. find the min of a consecutive array
            if n-1 in nums: continue
            # 3. expand rightwards
            start = n
            while n in nums: n += 1
            res = max(res, n-start)
        
        return res