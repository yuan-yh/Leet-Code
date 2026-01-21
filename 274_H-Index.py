# Method 1: No Sorting + PostSum
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        # Key Insight: h in range [0, len(citations)]
        # 1. count citation frequency
        length = len(citations)
        cnt = [0] * (length + 1)
        for c in citations:
            cnt[min(c, length)] += 1
        # 2. loop backwards
        res = pCnt = 0
        for c in range(len(citations), -1, -1):
            if res > c: break
            pCnt += cnt[c]
            res = max(res, min(pCnt, c))
        return res

        
# # Method 2: Sorting + Binary Search
# class Solution:
#     def hIndex(self, citations: List[int]) -> int:
#         # Key Insight: >= h paper + each paper has at least h citations, so h in [0, len(paper) + 1)
#         # 1. sort
#         citations.sort()
        
#         # 2. binary search: [left, right)
#         l, r, length = 0, len(citations) + 1, len(citations)
#         while l + 1 < r:
#             m = (l + r) >> 1
#             # H-idx = m, at least m papers each with m citations: cit[len - m] >= m
#             if citations[length - m] < m: r = m
#             else: l = m
#         return l