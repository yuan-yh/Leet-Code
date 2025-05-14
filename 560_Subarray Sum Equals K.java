// Time complexity : O(n)
// Space complexity : O(n)

class Solution {
    public int subarraySum(int[] nums, int k) {
        int count = 0, sum = 0;
        // <sum, count of subarray with this sum>
        Map<Integer, Integer> m = new HashMap<>();
        // init：前缀和为 0 出现 1 次（空子数组）
        m.put(0, 1);
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            // 检查是否存在前缀和等于 sum - k
            if (m.containsKey(sum - k)) count += m.get(sum - k);
            m.put(sum, m.getOrDefault(sum, 0) + 1);
        }
        return count;
    }
}