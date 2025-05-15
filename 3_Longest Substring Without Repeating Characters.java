// Time complexity: O(n)
// Space complexity: O(m)
// Where n is the length of the string and m is the total number of unique characters in the string.

class Solution {
    public int lengthOfLongestSubstring(String s) {
        // edge case: s.length <= 1
        if (s.length() <= 1) return s.length();

        int left = 0, res = 0, sLength = s.length();
        Map<Character, Integer> indexRecord = new HashMap<>();

        for (int right = 0; right < sLength; right++) {
            char tmp = s.charAt(right);
            // case 1: repeated -> jump to new left boundary
            if (indexRecord.containsKey(tmp) && left <= indexRecord.get(tmp)) {
                left = indexRecord.get(tmp) + 1;
            }
            // case 2: new char -> add into map
            indexRecord.put(tmp, right);
            res = Math.max(res, right - left + 1);
        }

        return res;
    }
}