// Time complexity : O(n)
// Space complexity : O(n)

// prefix sum: psum[0:i) + sum[i:j] = psum[0:j]
// Therefore, if sum[i:j] = k -> psum[0:j] - psum[0:i) = k
class Solution {
    public int subarraySum(int[] nums, int k) {
        int prefix = 0, res = 0;
        Map<Integer, Integer> m = new HashMap<>();
        m.put(0, 1);

        for (int n : nums) {
            // subsum_end - subsum_start = k, so ssum_start = ssum_end - k
            prefix += n;
            if (m.containsKey(prefix - k)) res += m.get(prefix - k);
            m.put(prefix, m.getOrDefault(prefix, 0) + 1);
        }
        return res;
    }
}