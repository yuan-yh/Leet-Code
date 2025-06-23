class Solution {
    public int climbStairs(int n) {
        int[] count = new int[2];
        // init
        count[0] = 1;   // distance 1: one way
        count[1] = 2;   // distance 2: two ways

        if (n <= 2) return count[n-1];

        for (int i = 3; i <= n; i++) {
            int tmp = count[0] + count[1];
            count[0] = count[1];
            count[1] = tmp;
        }

        return count[1];
    }
}