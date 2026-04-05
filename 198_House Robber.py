class Solution:
    def rob(self, nums: List[int]) -> int:
        r = nr = 0
        for n in nums:
            # for the rob case, you may choose to rob or not to max profit
            r, nr = max(nr + n, r), r
        
        return max(r, nr)