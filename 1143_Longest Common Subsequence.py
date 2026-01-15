# 1D DP Optimization
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # 1. assign text1 the shorter string
        if len(text1) > len(text2): text1, text2 = text2, text1
        # 2. loop through text2 and update dp[len(text1)], need an extra variable to record diagonally prev status
        dp = [0] * len(text1)
        for t2 in text2:
            diag = 0
            for i, t1 in enumerate(text1):
                tmp = dp[i]
                if t1 == t2: dp[i]  = diag + 1
                elif i > 0: dp[i] = max(dp[i], dp[i-1])
                diag = tmp
        return dp[-1]
        
# # 2D DP
# class Solution:
#     def longestCommonSubsequence(self, text1: str, text2: str) -> int:
#         dp = [[0] * (len(text2) + 1) for _ in range(1 + len(text1))]

#         for j, t2 in enumerate(text2):
#             for i, t1 in enumerate(text1):
#                 if t1 == t2: dp[i + 1][j + 1] = dp[i][j] + 1
#                 else: dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
#         return dp[-1][-1]