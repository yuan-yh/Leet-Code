// Time Complexity: O(n * 2^n) - 有 2^n个子集，所以搜索树有 2^n个叶子，每个叶子复制 path 需要 O(n) 的时间.
// Space Complexity: O(n)

class Solution {
    private List<List<Integer>> res = new ArrayList<>();
    private List<Integer> curPath = new ArrayList<>();
    private int[] nums;

    // // Method 1: choose or not choose
    // private void dfs(int idx, int end) {
    //     // end case
    //     if (idx == end) {
    //         res.add(new ArrayList<>(curPath));
    //         return;
    //     }
    //     // process
    //     // not choose
    //     dfs(idx + 1, end);
    //     // choose
    //     curPath.add(nums[idx]);
    //     dfs(idx + 1, end);
    //     curPath.remove(curPath.size() - 1);
    // }

    // Method 2: not choose or choose from a given range
    private void dfs(int start, int end) {
        // not choose
        res.add(new ArrayList<>(curPath));

        // choose from [start, end)
        for (int i = start; i < end; i++) {
            curPath.add(nums[i]);
            dfs(i + 1, end);
            curPath.remove(curPath.size() - 1);
        }
    }

    public List<List<Integer>> subsets(int[] nums) {
        this.nums = nums;
        dfs(0, nums.length);
        return this.res;
    }
}