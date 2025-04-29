// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int trap(int[] height) {
        if (height.length <= 2) return 0;

        int res = 0, l = 0, r = height.length - 1;
        int lMax = height[l], rMax = height[r];
        while (l < r) {
            // trap water based on the lower wall
            // 1. calculate trapped water
            // 2. update pointer
            // 3. update wall height
            if (lMax < rMax) {
                res += (lMax - height[l]);
                l++;
                lMax = Math.max(lMax, height[l]);
            }
            else {
                res += (rMax - height[r]);
                r--;
                rMax = Math.max(rMax, height[r]);
            }
        }
        return res;
    }
}