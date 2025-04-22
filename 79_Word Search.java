class Solution {
    private int row, col;
    private int[][] dir = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

    public boolean exist(char[][] board, String word) {
        row = board.length;
        col = board[0].length;

        for (int r = 0; r < row; r++) {
            for (int c = 0; c < col; c++) {
                if (dfs(board, word, r, c, 0)) return true;
            }
        }

        return false;
    }

    private boolean dfs(char[][] board, String word, int curRow, int curCol, int wIndex) {
        if (wIndex == word.length()) return true;

        if (curRow < 0 || curRow >= row || curCol < 0 || curCol >= col || word.charAt(wIndex) != board[curRow][curCol]) return false;

        board[curRow][curCol] = '#';
        boolean res = false;
        for (int[] d : dir) {
            int tmpRow = curRow + d[0], tmpCol = curCol + d[1];
            res = res || (dfs(board, word, tmpRow, tmpCol, wIndex + 1));
        }

        board[curRow][curCol] = word.charAt(wIndex);
        return res;
    }
}