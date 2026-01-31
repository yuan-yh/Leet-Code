class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        i, l = 0, len(nums)
        res = []

        while i < l:
            start = i
            # 1. shift i to the next consecutive start
            i += 1
            while i < l and nums[i] == nums[i-1] + 1: i += 1
            # 2. check for 2 appended cases
            if i == start+1: res.append(str(nums[start]))
            else: res.append(f"{nums[start]}->{nums[i-1]}")

        return res