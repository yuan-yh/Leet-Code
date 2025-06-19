// Backtracking (Visited Array)
// Time complexity: O(n!)
// Space complexity: O(n^2)

class Solution {
    private List<List<String>> res = new ArrayList<>();
    private char[][] board;
    private boolean[] col, posiDiagonal, negaDiagonal;

    public List<List<String>> solveNQueens(int n) {
        this.board = new char[n][n];
        this.col = new boolean[n];
        // all points at the same posiDiagonal share the same r+c val
        this.posiDiagonal = new boolean[n*2];
        // all points at the same negaDiagonal share the same r-c val
        this.negaDiagonal = new boolean[n*2];

        // 1. init the board
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                board[r][c] = '.';
            }
        }
        // 2. process
        bt(0, n);
        return res;
    }

    private void bt(int row, int length) {
        // end case
        if (row == length) {
            List<String> ans = new ArrayList<>();
            for (char[] r : board) ans.add(new String(r));
            res.add(ans);
            return;
        }

        for (int c = 0; c < length; c++) {
            // cut branch
            if (col[c] || posiDiagonal[row + c] || negaDiagonal[row-c+length-1]) continue;
            // process
            col[c] = true; 
            posiDiagonal[row + c] = true; 
            negaDiagonal[row-c+length-1] = true;
            board[row][c] = 'Q';
            bt(row + 1, length);
            // backtrack
            board[row][c] = '.';
            col[c] = false; 
            posiDiagonal[row + c] = false; 
            negaDiagonal[row-c+length-1] = false;
        }
    }
}