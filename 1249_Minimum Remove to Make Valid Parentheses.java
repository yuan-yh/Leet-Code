// Optimal Stack
// Time complexity: O(n)
// Space complexity: O(n)
class Solution {
    public String minRemoveToMakeValid(String s) {
        Stack<Integer> stack = new Stack<>();
        StringBuilder sb = new StringBuilder(s);

        // enque: record index of '(' and pop when meet ')'
        for (int i = 0; i < sb.length(); i++) {
            if (sb.charAt(i) == '(') stack.push(i);
            else if (sb.charAt(i) == ')') {
                // process unmatching ')'
                if (stack.isEmpty()) sb.setCharAt(i, '\0');
                else stack.pop();
            }
        }

        // deque: process unmatching '('
        while (!stack.isEmpty()) {
            sb.setCharAt(stack.pop(), '\0');
        }

        StringBuilder res = new StringBuilder();
        for (int i = 0; i < sb.length(); i++) {
            if (sb.charAt(i) != '\0') res.append(sb.charAt(i));
        }
        return res.toString();
    }
}

// Optimal Without Stack
// Time complexity: O(n)
// Space complexity: O(1) extra space, O(n) space for the output string.
class Solution {
    public String minRemoveToMakeValid(String s) {
        int leftP = 0, rightP = 0;

        // count ')'
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == ')') rightP ++;
        }

        // build the response
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            // For '(', skip if not enough ')'
            if (s.charAt(i) == '(') {
                // process unmatching '('
                if (leftP == rightP) continue;
                // process matching '('
                leftP++;
            }
            // For ')', skip if no '('; otherwise, process both '(' and ')'
            else if (s.charAt(i) == ')') {
                // process unmatching ')'
                if (leftP == 0) {
                    rightP--;
                    continue;
                }
                // process matching ')'
                else {
                    leftP--;
                    rightP--;
                }
            }

            sb.append(s.charAt(i));
        }

        return sb.toString();
    }
}