# Requirement: len(subarray) >= 2
# Key Insight: 对于任意长度 ≥ 3 的子数组 [a, ..., b]，它的 min + max 一定 ≤ 某个长度为 2 的相邻子数组的 min + max。

class Solution:
    def subarray_sum(self, nums) -> int:
        res = -inf
        for i, j in pairwise(nums):
            res = max(res, i+j)
        return res