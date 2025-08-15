class Solution {
    public int findLengthOfLCIS(int[] nums) {
        int res = 0, tmpLen = 1, tmpMax = nums[0];

        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > tmpMax) tmpLen++;
            else {
                res = Math.max(res, tmpLen);
                tmpLen = 1;
            }
            tmpMax = nums[i];
        }
        return Math.max(res, tmpLen);
    }
}