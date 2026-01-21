class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        res, buyin = 0, prices[0]

        for p in prices:
            if p < buyin: buyin = p
            res = max(res, p - buyin)
        
        return res