// Time Complexity: O(n^2)
// Space Complexity: O(n)

class Solution {
    private List<String> res = new ArrayList<>();

    public List<String> letterCasePermutation(String s) {
        if (s.length() > 0) bt(s.toCharArray(), 0);
        return res;
    }

    private void bt(char[] s, int start) {
        // end case
        if (start == s.length) {
            res.add(new String(s));
            return;
        }
        // process
        if (Character.isLetter(s[start])) {
            // 2 branches: lowercase & uppercase
            s[start] = Character.toLowerCase(s[start]);
            bt(s, start + 1);
            s[start] = Character.toUpperCase(s[start]);
            bt(s, start + 1);
        }
        else bt(s, start + 1);
        // backtrack
    }
}