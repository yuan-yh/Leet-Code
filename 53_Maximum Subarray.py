class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # The max subarray sum can be viewed as the height difference between bottom and peak.
        # Therefore, at each node, we can either +presum or restart as presum
        # However, if presum <= 0, the sum is always greater to restart;
        #          if presum > 0, the sum is always greater to continue to add.
        # Edge Case: all negative components
        res = presum = nums[0]

        for n in nums[1:]:
            # 1. update presum: continue to add or restart
            presum = max(n, presum + n)
            # 2. update res: current digit or presum
            res = max(res, presum)

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