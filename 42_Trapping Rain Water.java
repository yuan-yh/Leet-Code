// Time complexity: O(n)
// Space complexity: O(1)

// trap water based on the lower wall
// 1. calculate trapped water
// 2. update pointer
// 3. update wall height

class Solution {
    public int trap(int[] height) {
        int res = 0, l = 0, r = height.length - 1, lMax = height[0], rMax = height[height.length-1];

        while (l < r) {
            lMax = Math.max(lMax, height[l]);
            rMax = Math.max(rMax, height[r]);
            if (lMax < rMax) {
                res += lMax - height[l];
                l += 1;
            }
            else {
                res += rMax - height[r];
                r -= 1;
            }
        }
        return res;
    }
}