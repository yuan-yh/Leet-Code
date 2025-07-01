class Solution {
    private int[] nums;

    public int findTargetSumWays(int[] nums, int target) {
        // Method 1 (slow): binary tree - each branch is eith + or -
        // Method 2: 0-1背包 (DP)
        // sum of selected positive nums[i] = p
        // the absolute value for sum of selected negative nums[i] = q
        // p + q = complete array sum s
        // p - q = target t
        // Therefore, 
        // for target > 0 so p > q
        //  q = (s - t) / 2 => pack capacity = q as space optimization => how many ways to fill the backpack
        // OR for target < 0 so p < q
        //  p = (s + t) / 2 => pack capacity = p as space optimization => how many ways to fill the backpack
        // OVERALL: for backpack size optimization -> (s - abs(t)) / 2
        int s = 0;
        for (int n : nums) s += n;
        s -= Math.abs(target);
        // optimization
        if (s < 0 || s%2 == 1) return 0;
        s /= 2;     // backpack size
        this.nums = nums;
    }
}