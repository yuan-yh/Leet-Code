// Time Complexity: O(n * 2^n)
// Space Complexity: O(n)

// Thought: similar as LC78, can be considered as a tree
class Solution {
    List<List<String>> res = new ArrayList<>();
    List<String> cur = new ArrayList<>();

    public List<List<String>> partition(String s) {
        bt(s, 0);
        return res;
    }

    private void bt(String s, int start) {
        // end case
        if (start == s.length()) {
            res.add(new ArrayList<>(cur));
            return;
        }

        // check all palindromes after the cur char
        for (int end = start; end < s.length(); end++) {
            if (checkPalindrome(s, start, end)) {
                cur.add(s.substring(start, end + 1));
                bt(s, end + 1);
                cur.remove(cur.size() - 1);
            }
        }
    }

    private boolean checkPalindrome(String s, int start, int end) {
        if (start == end) return true;

        while (start < end) {
            if (s.charAt(start++) != s.charAt(end--)) return false;
        }
        return true;
    }
}