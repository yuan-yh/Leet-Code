class Solution {
    public int rob(int[] nums) {
        // plan[0]: max profit if rob the cur house
        // plan[1]: max profit if not rob the cur house

        // init
        int[] plan = new int[2];
        plan[0] = nums[0];
        plan[1] = 0;

        for (int i = 1; i < nums.length; i++) {
            int tmp = Math.max(plan[0], plan[1]);
            plan[0] = plan[1] + nums[i];
            plan[1] = tmp;
        }

        return Math.max(plan[0], plan[1]);
    }
}