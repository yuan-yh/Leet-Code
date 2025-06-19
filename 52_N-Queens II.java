// Time complexity: O(n!)
// Space complexity: O(n^2)

class Solution {
    private int count = 0;
    private boolean[] col, posiDiagonal, negaDiagonal;

    public int totalNQueens(int n) {
        // init
        this.col = new boolean[n];
        this.posiDiagonal = new boolean[2*n];
        this.negaDiagonal = new boolean[2*n];
        // process
        bt(0, n);
        return count;
    }

    private void bt(int row, int length) {
        // end case
        if (row == length) {
            count ++;
            return;
        }

        for (int c = 0; c < length; c++) {
            // cut branch
            if (col[c] || posiDiagonal[row+c] || negaDiagonal[row-c+length-1]) continue;
            // process
            col[c] = true; 
            posiDiagonal[row+c] = true; 
            negaDiagonal[row-c+length-1] = true; 
            bt(row+1, length);
            // retrieve
            col[c] = false; 
            posiDiagonal[row+c] = false; 
            negaDiagonal[row-c+length-1] = false; 
        }
    }
}