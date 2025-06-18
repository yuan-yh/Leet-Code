// Time Complexity: O(n * C(2n,n))
// Space Complexity: O(n)

class Solution {
    private List<String> res = new ArrayList<>();
    private StringBuilder sb;

    public List<String> generateParenthesis(int n) {
        this.sb = new StringBuilder(n*2);
        bt(n, 0);
        return res;
    }

    private void bt(int openCanBePlaced, int closeCanBePlaced) {
        // end case
        if (openCanBePlaced == 0 && closeCanBePlaced == 0) {
            res.add(sb.toString());
            return;
        }
        // process
        // backtrack
        if (openCanBePlaced > 0) {
            sb.append('(');
            bt(openCanBePlaced-1, closeCanBePlaced+1);
            sb.deleteCharAt(sb.length() - 1);
        }
        if (closeCanBePlaced > 0) {
            sb.append(')');
            bt(openCanBePlaced, closeCanBePlaced-1);
            sb.deleteCharAt(sb.length() - 1);
        }
    }
}