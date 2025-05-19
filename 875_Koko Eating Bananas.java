// Time complexity: O(nlogU)，其中 n 为 piles 的长度，U=max(piles)。
// Space complexity: O(1)

class Solution {
    public int minEatingSpeed(int[] piles, int h) {
        // 1. k in the range [1, max(piles[i])]
        int left = 1, right = -1;
        for (int p : piles) right = Math.max(right, p);

        // edge case: piles.length == h
        if (piles.length == h) return right;

        // 2. binary search in [left, right]: return the first element that returns true
        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (check(piles, h, mid)) right = mid - 1;  // right+1: BLUE
            else left = mid + 1;                        // left-1: RED
        }
        return left;
    }

    private boolean check(int[] piles, int h, int k) {
        // time for piles[i] = (piles[i] / k) + (piles[i] % k != 0) ? 1 : 0
        long time = 0;
        for (int p : piles) time += (p / k) + ((p % k != 0) ? 1 : 0);
        return (time <= h);
    }
}