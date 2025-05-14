// Time complexity : O(n)
// Space complexity : O(n)

// prefix sum: psum[0:i) + sum[i:j] = psum[0:j]
// Therefore, if sum[i:j] = k -> psum[0:j] - psum[0:i) = k
class Solution {
    public int subarraySum(int[] nums, int k) {
        int count = 0, sum = 0;
        Map<Integer, Integer> m = new HashMap<>();  // <psum, count>
        m.put(0, 1);

        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            if (m.containsKey(sum - k)) count += m.get(sum - k);
            m.put(sum, m.getOrDefault(sum, 0) + 1);
        }

        return count;
    }
}