// 时间复杂度：O(n)，其中 n 是 nums 的长度。
// 空间复杂度：O(m)。其中 m 是 nums 中的不同元素个数。

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> nset = new HashSet<>();
        for (int n : nums) nset.add(n);
        int res = 0;

        for (int n : nset) {
            // skip if not the start of a consecutive sequence
            if (nset.contains(n-1)) continue;
            int start = n;
            while (nset.contains(n)) n++;
            res = Math.max(res, n-start);
        }
        return res;
    }
}