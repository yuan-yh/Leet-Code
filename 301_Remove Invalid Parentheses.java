class Solution {
    private Set<String> res = new HashSet<>();
    private StringBuilder sb = new StringBuilder();

    public List<String> removeInvalidParentheses(String s) {
        // 1. count open/close parenthesis to be removed
        int openDel = 0, closeDel = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') openDel++;
            else if (c == ')') {
                if (openDel > 0) openDel--;
                else closeDel++;
            }
        }
        // 2. backtrack
        bt(s, 0, openDel, closeDel, 0);
        return new ArrayList<>(res);
    }

    private void bt(String s, int index, int openDel, int closeDel, int curOpenCount) {
        // end case
        if (index == s.length()) {
            if (openDel == 0 && closeDel == 0) res.add(sb.toString());
            return;
        }
        // process & backtrack
        char cur = s.charAt(index);
        // branch: del
        if (cur == '(' && openDel > 0) bt(s, index+1, openDel-1, closeDel, curOpenCount);
        else if (cur == ')' && closeDel > 0) bt(s, index+1, openDel, closeDel-1, curOpenCount);
        // branch: NOT del
        sb.append(cur);
        if (cur == '(') bt(s, index+1, openDel, closeDel, curOpenCount+1);
        else if (cur == ')') {
            if (curOpenCount > 0) bt(s, index+1, openDel, closeDel, curOpenCount-1); // cut branch
        }
        else bt(s, index+1, openDel, closeDel, curOpenCount); // cur char is not open/close parenthesis -> pass
        sb.deleteCharAt(sb.length() - 1);
    }
}