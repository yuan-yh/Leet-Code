// 时间复杂度：O(n)，其中 n 为 nums 的长度。由于每个下标至多入队出队各一次，所以二重循环的循环次数是 O(n) 的。
// 空间复杂度：O(min(k,U))，其中 U 是 nums 中的不同元素个数（本题至多为 20001）。
// 双端队列至多有 k 个元素，同时又没有重复元素，所以也至多有 U 个元素，所以空间复杂度为 O(min(k,U))。返回值的空间不计入。


class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        Deque<Integer> q = new ArrayDeque<>();
        int[] res = new int[nums.length - k + 1];

        for (int i = 0; i < nums.length; i++) {
            // case: cur >= pre -> remove then attach
            // case: cur < pre -> attach
            while (!q.isEmpty() && nums[q.getLast()] <= nums[i]) q.removeLast();
            q.addLast(i);
            // validate window & record & expire window start if head
            int start = i - k + 1;
            if (start >= 0) {
                res[start] = nums[q.getFirst()];
                if (start == q.getFirst()) q.removeFirst();
            }
        }

        return res;
    }
}