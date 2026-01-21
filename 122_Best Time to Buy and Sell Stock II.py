class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Greedy: earn all potential profits in past days, then get lower prices for the future
        # 把一次大涨拆成多次小涨，收入每次小涨
        res, buyin = 0, prices[0]

        for p in prices:
            if p >= buyin: res += p - buyin
            buyin = p
        return res