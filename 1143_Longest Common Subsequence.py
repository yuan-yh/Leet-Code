# 1D DP Optimization
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # 1. assign text1 the shorter string
        if len(text1) > len(text2): text1, text2 = text2, text1
        # 2. dp[i] - max LCS for text1[:i] inclusively and text2[:j] inclusively during the loop
        dp = [0] * len(text1)

        for j, t2 in enumerate(text2):
            prev = 0 # diagonal dp[i-1][j-1]
            for i, t1 in enumerate(text1):
                tmp = dp[i]
                if t1 == t2: dp[i] = prev + 1
                elif i > 0: dp[i] = max(dp[i], dp[i-1])
                prev = tmp
        return dp[-1]

# # 2D DP
# class Solution:
#     def longestCommonSubsequence(self, text1: str, text2: str) -> int:
#         l1, l2 = len(text1), len(text2)
#         dp = [[0] * (l2 + 1) for _ in range(l1 + 1)]

#         for j, t2 in enumerate(text2):
#             for i, t1 in enumerate(text1):
#                 if t1 == t2: dp[i+1][j+1] = dp[i][j] + 1
#                 else: dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
#         return dp[l1][l2]