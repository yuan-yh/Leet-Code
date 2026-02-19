// 时间复杂度：O(∣Σ∣m+n)，其中 m 是 s 的长度，n 是 p 的长度，∣Σ∣=26 是字符集合的大小。
// 空间复杂度：O(∣Σ∣)。返回值不计入

class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();

        // 1. count p
        char[] pCnt = new char[26];
        for (char c : p.toCharArray()) pCnt[c-'a'] += 1;

        // 2. init s count
        char[] sCnt = new char[26];
        // 3. loop s
        for (int end = 0; end < s.length(); end++) {
            // 4. update s count
            sCnt[s.charAt(end) - 'a'] += 1;

            // 5. check if long-enough window
            int start = end - p.length() + 1;
            if (start < 0) continue;

            // 6. check for matching window
            if (Arrays.equals(pCnt, sCnt)) res.add(start);

            // 7. expire letters not-shown in the next window
            sCnt[s.charAt(start) - 'a'] -= 1;

        }
        return res;
    }
}