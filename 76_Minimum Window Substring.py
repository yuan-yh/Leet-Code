# Method 1: use hashmap & int_variable to track different letters
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # 1. count t letter into hashmap
        tCnt = defaultdict(int)
        for c in t: tCnt[c] += 1
        # 2. declare number of letters missed
        miss = len(tCnt)
        
        # 3. loop s with window end
        start, resL, resR = 0, -1, len(s)
        for end, c in enumerate(s):
            # 4. update tCnt & decrement miss when zero_count
            tCnt[c] -= 1
            if tCnt[c] == 0: miss -= 1
            # 5. while no missing, update res & shrink the window start until miss > 0
            while miss == 0:
                if end-start < resR-resL: resL, resR = start, end
                tCnt[s[start]] += 1
                if tCnt[s[start]] > 0: miss += 1
                start += 1

        return "" if resL < 0 else s[resL:resR+1]

# # Method 2: use Counter()
# class Solution:
#     def minWindow(self, s: str, t: str) -> str:
#         # Sliding window: expand right until satisfied, then shrink left until unsatisfied
#         resL, resR = -1, len(s)
#         tCnt = Counter(t)
#         sCnt = Counter()
#         left = 0

#         for right, c in enumerate(s):
#             # 1. update sCnt
#             sCnt[c] += 1
#             # 2. compare w/ tCnt
#             while sCnt >= tCnt:
#                 # 3. while match, update res & shrink left
#                 if right-left < resR-resL: resL, resR = left, right
#                 sCnt[s[left]] -= 1
#                 left += 1

#         return "" if resL == -1 else s[resL : resR + 1]