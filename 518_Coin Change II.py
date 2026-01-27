class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        bag = [1] + [0] * amount

        for c in coins:
            for i in range(c, amount + 1):
                if bag[i-c] != 0: bag[i] += bag[i-c]
        return bag[-1]