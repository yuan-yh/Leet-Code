// Time complexity: O(n)
// Space complexity: O(1)

// trap water based on the lower wall
// 1. calculate trapped water
// 2. update pointer
// 3. update wall height

class Solution {
    public int trap(int[] height) {
        if (height.length < 2) return 0;
        
        int left = 0, right = height.length - 1, res = 0; 
        int lWall = height[left], rWall = height[right];

        while (left < right) {
            // 1. shift left wall
            if (lWall < rWall) {
                res += (lWall - height[left]);
                left ++;
                lWall = Math.max(lWall, height[left]);
            }
            // 2. shift right wall
            else {
                res += (rWall - height[right]);
                right --;
                rWall = Math.max(rWall, height[right]);
            }
        }
        return res;
    }
}