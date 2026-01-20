class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # DP: at nums[i], either + prevSum or restart from itself
        res = curSum = nums[0]
        for i in nums[1:]:
            curSum = max(curSum + i, i)
            res = max(res, curSum)
        return res

# # Greedy + DP
# class Solution:
#     def maxSubArray(self, nums: List[int]) -> int:
#         # For nums[i], either continue to add or restart from itself
#         # except the edge case of all negative, once negative -> discard
#         res, curSum = -inf, 0
#         for i in nums:
#             res = max(res, curSum + i, i)
#             if curSum + i >= 0: curSum += i
#             else: curSum = 0
#         return res