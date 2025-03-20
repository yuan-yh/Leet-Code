// Time complexity: O(n)
// Space complexity: O(n)

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        // Bucket Sort
        // 1. count frequency
        Map<Integer, Integer> count = new HashMap<>();
        for (int i : nums) count.put(i, count.getOrDefault(i, 0) + 1);
        // 2. sort based on frequency - place into buckets
        List<Integer>[] bucket = new List[nums.length + 1];
        for (int i = 0; i <= nums.length; i++) bucket[i] = new ArrayList<>();
        for (Map.Entry<Integer, Integer> entry : count.entrySet()) {
            int curNum = entry.getKey(), curCount = entry.getValue();
            bucket[curCount].add(curNum);
        }
        // 3. iterate backwards through buckets
        int[] res = new int[k];
        int index = 0;
        for (int i = nums.length; i > 0; i--) {
            for (int j : bucket[i]) {
                res[index] = j;
                index ++;
                if (index == k) return res;
            }
        }
        return res;
    }
}