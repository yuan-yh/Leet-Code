class Solution {
    public int maxArea(int[] height) {
        int res = 0, l = 0, r = height.length - 1;
        int lMax = height[l], rMax = height[r];
        while (l < r) {
            // compare the wall height, then calculate the container area based on the lower wall
            if (lMax < rMax) {
                res = Math.max(res, lMax*(r - l));
                l++;
                lMax = Math.max(lMax, height[l]);
            }
            else {
                res = Math.max(res, rMax*(r - l));
                r--;
                rMax = Math.max(rMax, height[r]);
            }
        }
        return res;
    }
}