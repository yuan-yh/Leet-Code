// Time complexity: O(m+n) 或 O(m+n+∣Σ∣)，其中 m 为 s 的长度，n 为 t 的长度，∣Σ∣=128。
// Space complexity: O(∣Σ∣)。如果创建了大小为 128 的数组，则 ∣Σ∣=128

class Solution {
    public String minWindow(String s, String t) {
        int[] tCount = new int[128];
        int tUniqueCharCount = 0;

        // 1. count letter in t
        for (int i = 0; i < t.length(); i++) {
            if (tCount[t.charAt(i)] == 0) tUniqueCharCount++;
            tCount[t.charAt(i)]++;
        }

        // 2. sliding window in s
        int left = 0, resLeft = -1, resRight = s.length();

        for (int right = 0; right < s.length(); right++) {
            char cur = s.charAt(right);
            tCount[cur] --;

            // update the tUniqueCharCount
            if (tCount[cur] == 0) tUniqueCharCount--;

            // process the substring which meets the requirement
            while (tUniqueCharCount == 0) {
                // update the minimum window length
                if (right - left < resRight - resLeft) {
                    resLeft = left;
                    resRight = right;
                }

                // shift the left pointer
                char tmp = s.charAt(left);
                // 既然tmp出現次數為0，且s含有tmp；説明t也有tmp而且這個tmp滿足了substring條件
                if (tCount[tmp] == 0) tUniqueCharCount ++;
                tCount[tmp] ++;
                left ++;
            }
        }

        return (resLeft == -1 || resRight == s.length()) ? "" : s.substring(resLeft, resRight + 1);
    }
}