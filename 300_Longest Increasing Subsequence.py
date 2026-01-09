# Greedy + Binary Search: O(n log n)
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        minEnd = [nums[0]]  # minEnd[i] is the min end digit for the increasing subsequence w/ length i+1

        for n in nums[1:]:
            # for max j such that minEnd[j] >= n -> replace w/ n or expand the subsequence by appending n
            # Therefore, binary search (start, end]
            l, r = -1, len(minEnd)
            while l + 1 < r:
                m = (l + r) >> 1
                if minEnd[m] >= n: r = m
                else: l = m
            
            if r == len(minEnd): minEnd.append(n)
            else: minEnd[r] = n
        return len(minEnd)

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