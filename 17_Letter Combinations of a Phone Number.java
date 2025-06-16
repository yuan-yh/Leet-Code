// Time Complexity: O(n * 4^n)
// Space Complexity: O(n)

class Solution {
    private char[][] table = {{'a', 'b', 'c'}, {'d', 'e', 'f'}, {'g', 'h', 'i'}, 
        {'j', 'k', 'l'}, {'m', 'n', 'o'}, {'p', 'q', 'r', 's'}, {'t', 'u', 'v'}, {'w', 'x', 'y', 'z'}};
    private List<String> res = new ArrayList<>();
    private StringBuilder cur = new StringBuilder(4);

    public List<String> letterCombinations(String digits) {
        if (digits.length() > 0) bt(digits, 0);
        return res;
    }

    private void bt(String digits, int start) {
        // end case
        if (start == digits.length()) {
            res.add(cur.toString());
            return;
        }

        for (int i = 0; i < table[(digits.charAt(start) - '2')].length; i++) {
            // process
            cur.append(table[(digits.charAt(start) - '2')][i]);
            bt(digits, start + 1);
            // retrieve
            cur.deleteCharAt(cur.length() - 1);
        }
    }
}