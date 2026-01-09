class Solution:
    def uniquePaths(self, row: int, col: int) -> int:
        dp_col = [1] * row # update from column to column

        for c in range(1, col):
            for r in range(1, row):
                dp_col[r] += dp_col[r-1]
        return dp_col[-1]