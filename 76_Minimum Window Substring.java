// https://leetcode.cn/problems/minimum-window-substring/solutions/2713911/liang-chong-fang-fa-cong-o52mn-dao-omnfu-3ezz/
// Still can be optimized
// Time complexity: O(∣Σ∣m+n)，其中 m 为 s 的长度，n 为 t 的长度，∣Σ∣ 为字符集合的大小 (52)
// Space complexity: O(∣Σ∣)。如果创建了大小为 128 的数组，则 ∣Σ∣=128

class Solution {
    public String minWindow(String s, String t) {
        // 1. count char in t
        int[] tCount = new int[128];
        for (int i = 0; i < t.length(); i++) {
            tCount[t.charAt(i)] ++;
        }
        // 2. sliding window on s
        int[] sCount = new int[128];
        int left = 0, resLeft = -1, resRight = s.length();
        for (int right = 0; right < s.length(); right++) {
            sCount[s.charAt(right)]++;

            // shift the left pointer & update res
            while (isCovered(tCount, sCount)) {
                // update res
                if (resRight - resLeft > right - left) {
                    resRight = right;
                    resLeft = left;
                }
                // shift the left pointer
                sCount[s.charAt(left)]--;
                left++;
            }
        }

        return (resLeft == -1 || resRight == s.length()) ? "" : s.substring(resLeft, resRight+1);
    }

    private Boolean isCovered(int[] tCount, int[] sCount) {
        for (int i = 'a'; i <= 'z'; i++) {
            if (sCount[i] < tCount[i]) return false;
        }
        for (int i = 'A'; i <= 'Z'; i++) {
            if (sCount[i] < tCount[i]) return false;
        }
        return true;
    }
}