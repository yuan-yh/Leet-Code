// Time complexity: O(m+n) 或 O(m+n+∣Σ∣)，其中 m 为 s 的长度，n 为 t 的长度，∣Σ∣=128。
// Space complexity: O(∣Σ∣)。如果创建了大小为 128 的数组，则 ∣Σ∣=128

class Solution {
    public String minWindow(String s, String t) {
        // 1. count t letter freq & unique letter to track missing
        int[] tCnt = new int[128];
        int miss = 0;
        for (char c : t.toCharArray()) {
            if (tCnt[c] == 0) miss += 1;
            tCnt[c] += 1;
        }

        // 2. loop s through window end
        int start = 0, resL = -1, resR = s.length();

        for (int end = 0; end < s.length(); end ++) {
            // 3. update the count of cur letter & miss if tCnt[cur] == 0
            tCnt[s.charAt(end)] -= 1;
            if (tCnt[s.charAt(end)] == 0) miss -= 1;

            // 4. when satisfy: update res & shrink the window start
            while (miss == 0) {
                if (end-start < resR-resL) {
                    resL = start;
                    resR = end;
                }
                tCnt[s.charAt(start)] += 1;
                if (tCnt[s.charAt(start)] > 0) miss += 1;
                start += 1;
            }
        }

        return resL == -1 ? "" : s.substring(resL, resR + 1);
    }
}