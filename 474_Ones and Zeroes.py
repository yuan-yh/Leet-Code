class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        # cnt of 0s and 1s must be inspected together -> 2D Bag
        bag = [[0] * (n + 1) for _ in range(m + 1)] # row: 0s; col: 1s

        for s in strs:
            c0, c1 = s.count('0'), s.count('1')
            for r in range(m, c0-1, -1):
                for c in range(n, c1-1, -1):
                    bag[r][c] = max(bag[r][c], bag[r-c0][c-c1] + 1)
        return bag[-1][-1]