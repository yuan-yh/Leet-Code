class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # The max subarray sum can be viewed as the height difference between bottom and peak.
        # Therefore, at each node, we can either +presum or restart as presum
        # However, if presum <= 0, the sum is always greater to restart;
        #          if presum > 0, the sum is always greater to continue to add.
        # Edge Case: all negative components
        
        # Prefix Sum + Greedy
        res, curSum = -inf, 0
        # Case: all negative || non-negative
        for n in nums:
            # case: single digit
            res = max(res, n)
            # case: subarray
            curSum += n
            if curSum < 0: curSum = 0
            else: res = max(res, curSum)

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