// Time complexity: O(n)
// Space complexity: O(m)
// Where n is the length of the string and m is the total number of unique characters in the string.

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> m = new HashMap<>();
        int res = 0, start = 0;

        for (int end = 0; end < s.length(); end++) {
            // case: repeat in the cur window -> shift start
            if (m.containsKey(s.charAt(end)) && m.get(s.charAt(end)) >= start) {
                start = m.get(s.charAt(end)) + 1;
            }
            // update hashmap
            m.put(s.charAt(end), end);
            // update res
            res = Math.max(res, end - start + 1);
        }

        return res;
    }
}