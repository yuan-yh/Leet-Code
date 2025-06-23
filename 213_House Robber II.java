class Solution {
    public int rob(int[] nums) {
        if (nums.length == 1) return nums[0];
        
        int notRobFirst, notRobLast, tmp;
        // record[0] - not rob; record[1] - rob
        int[] record = new int[2];

        // case 1: not rob first
        for (int i = 1; i < nums.length; i++) {
            tmp = Math.max(record[0], record[1]);
            record[1] = record[0] + nums[i];
            record[0] = tmp;
        }
        notRobFirst = Math.max(record[0], record[1]);

        // case 2: not rob last
        record[0] = 0;
        record[1] = nums[0];
        for (int i = 1; i < nums.length; i++) {
            tmp = Math.max(record[0], record[1]);
            record[1] = record[0] + nums[i];
            record[0] = tmp;
        }
        notRobLast = record[0];

        return Math.max(notRobFirst, notRobLast);
    }
}