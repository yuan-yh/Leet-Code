// Time Complexity: O(n * 2^n)
// Space Complexity: O(n)

// Method 1
class Solution {
    List<List<Integer>> res = new ArrayList<>();
    List<Integer> cur = new ArrayList<>();

    public List<List<Integer>> subsets(int[] nums) {
        bt(nums, 0);        
        return res;
    }

    private void bt(int[] nums, int start) {
        // end case
        if (start == nums.length) {
            res.add(new ArrayList<>(cur));
            return;
        }

        // case 1: not add cur digit
        bt(nums, start + 1);

        // case 2: add cur digit
        cur.add(nums[start]);
        bt(nums, start + 1);
        cur.remove(cur.size() - 1);
    }
}