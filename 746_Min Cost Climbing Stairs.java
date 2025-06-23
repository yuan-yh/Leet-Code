class Solution {
    public int minCostClimbingStairs(int[] cost) {
        int[] stair = new int[2];
        
        // init: stair[0] = stair[1] = 0
        for (int i = 2; i <= cost.length; i++) {
            int tmp = Math.min(cost[i-2]+stair[0], cost[i-1]+stair[1]);
            stair[0] = stair[1];
            stair[1] = tmp;
        }
        return stair[1];
    }
}