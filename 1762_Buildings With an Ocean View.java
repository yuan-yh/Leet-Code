// Monotonic Stack Space Optimization
// Time complexity: O(N)
// Space complexity: O(N) for Java, O(1) for Python
// In Java, in order to maintain a dynamic size array (since we don't know the size of the output array at the beginning), we created an extra Array List that supports fast O(1) push operation. Array List can contain at most N elements, hence for the Java solution, the space complexity is O(N).

class Solution {
    public int[] findBuildings(int[] heights) {
        int l = heights.length, maxHeight = -1;
        List<Integer> list = new ArrayList<>();

        for (int i = l-1; i >= 0; i--) {
            if (heights[i] > maxHeight) {
                list.add(i);
                maxHeight = heights[i];
            }
        }

        int[] res = new int[list.size()];
        for (int j = 0; j < list.size(); j++) {
            res[j] = list.get(list.size() - j - 1);
        }

        return res;
    }
}