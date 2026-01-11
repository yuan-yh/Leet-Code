# Greedy + Binary Search: O(n log n)
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # dp[i]: the min end of LIS w/ size i+1, must be sorted so we can use Binary Search
        dp = []

        for n in nums:
            # n > all dp[i]: append to build a longer LIS
            # n <= dp[i]: replace w/ n
            l, r = -1, len(dp)      # (start, end]
            while l + 1 < r:
                m = (l + r) >> 1
                if dp[m] < n: l = m
                else: r = m
            
            if r == len(dp): dp.append(n)
            else: dp[r] = n

        return len(dp)

# # Heap: O(n^2)
# class Solution:
#     def lengthOfLIS(self, nums: List[int]) -> int:
#         # dp[i] is the max length of the longest strictly increasing subsequence ending in nums[i]
#         # dp[i] = max(dp[j] + 1) for j < i and nums[j] < nums[i]
#         res, n = 0, len(nums)
#         if n <= 1: return n

#         heap = []
#         dp = [0] * n

#         def find(idx) -> int:
#             tmp = heap[:]
#             while tmp:
#                 prevL, prevN = heappop(tmp)
#                 if prevN < nums[idx]: return -prevL
#             return 0

#         for i in range(n):
#             prevL = find(i)
#             dp[i] = prevL + 1
#             heappush(heap, (-dp[i], nums[i]))
#             res = max(res, dp[i])
#         return res