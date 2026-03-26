// Backtracking (Optimal)
// Time complexity: O(n!∗n)
// Space complexity: O(n!∗n) for the output list

// Method 1
class Solution {
    List<List<Integer>> res;

    public List<List<Integer>> permute(int[] nums) {
        res = new ArrayList<>();
        backtrack(nums, 0);
        return res;
    }

    private void backtrack(int[] nums, int index) {
        // all digits in the nums array before 'index' have been added into the current path
        // end case: complete the re-arrangment of nums
        if (index == nums.length) {
            List<Integer> list = new ArrayList<>();
            for (int n : nums) list.add(n);
            res.add(list);
            return;
        }
        // process & retrieve
        for (int i = index; i < nums.length; i++) {
            swap(nums, i, index);   // determine the digit at index i
            backtrack(nums, index + 1);
            swap(nums, i, index);   // backtrack
        }
    }

    private void swap(int[] nums, int p1, int p2) {
        int tmp = nums[p1];
        nums[p1] = nums[p2];
        nums[p2] = tmp;
    }
}

// Method 2
class Solution {
    private List<List<Integer>> res;
    private List<Integer> curPath;
    private int[] nums;
    private boolean[] visit;
    private int length;

    private void bt() {
        // end case
        if (curPath.size() == this.length) {
            this.res.add(new ArrayList<>(curPath));
            return;
        }
        // process
        for (int i = 0; i < length; i++) {
            if (!visit[i]) {
                visit[i] = true;
                curPath.add(nums[i]);
                bt();
                curPath.remove(curPath.size() - 1);            
                visit[i] = false;
            }
        }
    }

    public List<List<Integer>> permute(int[] nums) {
        this.nums = nums;
        this.length = nums.length;
        this.visit = new boolean[length];
        this.curPath = new ArrayList<>();
        this.res = new ArrayList<>();

        bt();

        return this.res;
    }
}