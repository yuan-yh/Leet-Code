// Time complexity: O(n)
// Space complexity: O(m)
// Where n is the length of the string and m is the total number of unique characters in the string.

class Solution {
    public int lengthOfLongestSubstring(String s) {
        int left = 0, res = 0;
        Map<Character, Integer> m = new HashMap<>();

        for (int right = 0; right < s.length(); right++) {
            if (m.containsKey(s.charAt(right))) {
                left = Math.max(left, m.get(s.charAt(right)) + 1);
            }
            m.put(s.charAt(right), right);
            res = Math.max(res, right - left + 1);
        }

        return res;
    }
}