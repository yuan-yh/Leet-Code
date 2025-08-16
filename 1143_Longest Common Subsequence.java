class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int l1 = text1.length(), l2 = text2.length(), res = 0;
        int[][] dp = new int[l1+1][l2+1];

        for (int i = 1; i <= l1; i++) {
            for (int j = 1; j <= l2; j++) {
                if (dp[i][j-1] == i) {
                    dp[i][j] = dp[i][j-1];
                    continue;
                } 


                if (text1.charAt(i-1) == text2.charAt(j-1)) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                    res = Math.max(res, dp[i][j]);
                } else {
                    dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        return res;
    }
}