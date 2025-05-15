// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1, area = 0;

        // shift the pointer with lower boundary
        while (left < right) {
            area = Math.max(area, Math.min(height[left], height[right]) * (right - left));
            // lower left wall
            if (height[left] < height[right]) left ++;
            // lower right wall
            else right --;
        }

        return area;
    }
}