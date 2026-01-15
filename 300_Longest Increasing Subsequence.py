class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # Greedy: minimize the subsequence end at length i+1
        lcis = []

        for n in nums:
            # Binary Search to find i such that lcis[i] >= n then replace; if not append to end
            l, r = -1, len(lcis)    # (start, end]

            while l + 1 < r:
                m = (l + r) >> 1
                if lcis[m] >= n: r = m
                else: l = m
            
            if r == len(lcis): lcis.append(n)
            else: lcis[r] = n
        return len(lcis)