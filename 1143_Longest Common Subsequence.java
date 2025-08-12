class Solution {
    private int[][] record;
    private String s1;
    private String s2;

    public int longestCommonSubsequence(String text1, String text2) {
        int l1 = text1.length(), l2 = text2.length();
        this.s1 = text1;
        this.s2 = text2;
        this.record = new int[l1][l2];

        // init
        for (int i = 0; i < l1; i++) {
            for (int j  = 0; j < l2; j++) {
                record[i][j] = -1;
            }
        }

        return dfs(text1.length()-1, text2.length()-1);
    }

    private int dfs(int i, int j) {
        // end case
        if (i < 0 || j < 0) return 0;
        if (record[i][j] != -1) return record[i][j];

        // process
        int res = 0;
        if (s1.charAt(i) == s2.charAt(j)) res = (1+dfs(i-1, j-1));
        else res = Math.max(dfs(i-1, j), dfs(i, j-1));
        record[i][j] = res;
        return res;
    }
}