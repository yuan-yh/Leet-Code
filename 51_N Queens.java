// Backtracking (Visited Array)
// Time complexity: O(n!)
// Space complexity: O(n^2)

class Solution {
    List<List<String>> res;
    char[][] board;
    boolean[] col, posiDiagonal, negaDiagonal;

    public List<List<String>> solveNQueens(int n) {
        res = new ArrayList<>();
        board = new char[n][n];
        col = new boolean[n];
        // number of possible diagonals = 2*n - 1
        posiDiagonal = new boolean[2*n];
        negaDiagonal = new boolean[2*n];

        // init the board
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                board[r][c] = '.';
            }
        }
        // process w/ backtracking
        backtrack(0, n);

        return res;
    }

    private void backtrack(int rowPlaced, int total) {
        // end cases: all Queens placed
        if (rowPlaced == total) {
            // convert each board row into a string
            List<String> list = new ArrayList<>();
            for (char[] row : board) list.add(new String(row));
            res.add(list);
            return;
        }

        // process & backtrack
        for (int c = 0; c < total; c++) {
            // check if we can place a Queen at the row rowPlaced and the col c
            // for grids on the same positive diagonal, they have the same **(row+col)**
            // for grids on the same negative diagonal, they have the same **(row-col+n)**
            // Given the default init is false, true - a Queen has been placed on the col / diagonal
            if (col[c] || posiDiagonal[rowPlaced + c] || negaDiagonal[rowPlaced - c + total]) continue;

            // place the Queen & update col / diagonal
            board[rowPlaced][c] = 'Q';
            col[c] = true;
            posiDiagonal[rowPlaced + c] = true;
            negaDiagonal[rowPlaced - c + total] = true;

            backtrack(rowPlaced + 1, total);

            // backtrack / cancel the placement
            board[rowPlaced][c] = '.';
            col[c] = false;
            posiDiagonal[rowPlaced + c] = false;
            negaDiagonal[rowPlaced - c + total] = false;
        }
    }
}