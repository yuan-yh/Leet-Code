// Time complexity: O(n)
// Space complexity: O(n)

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> record = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            if (record.containsKey(nums[i])) return new int[]{record.get(nums[i]), i};
            record.put(target - nums[i], i);
        }
        return new int[]{-1, -1};
    }
}