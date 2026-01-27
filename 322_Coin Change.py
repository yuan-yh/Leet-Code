class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount <= 0: return 0

        # DP: 完全背包
        bag = [0] + [inf] * amount
        for c in coins:
            for i in range(c, amount+1):
                if bag[i-c] != inf: bag[i] = min(bag[i], bag[i-c] + 1)
        return -1 if bag[-1] == inf else bag[-1]