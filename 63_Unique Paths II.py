class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        row, col = len(obstacleGrid), len(obstacleGrid[0])
        if obstacleGrid[0][0] == 1 or obstacleGrid[row-1][col-1] == 1: return 0

        # init the first column
        dp_col = [1] * row
        for i in range(1, row):
            dp_col[i] = 0 if obstacleGrid[i][0] == 1 else dp_col[i-1]
        
        # update
        for c in range(1, col):
            for r in range(row):
                if obstacleGrid[r][c] == 1: dp_col[r] = 0
                elif r > 0: dp_col[r] += dp_col[r-1]

        return dp_col[row-1]