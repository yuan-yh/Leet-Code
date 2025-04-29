// 在遇到下一個operator時處理前一個的運算
// Solution: Optimised Approach without the stack
// Time Complexity: O(n)
// Space Complexity: O(1)

class Solution {
    public int calculate(String s) {
        if (s == null || s.length() == 0) return 0;

        int cur = 0, last = 0, res = 0;
        Character operator = '+';

        for (int i = 0; i < s.length(); i++) {
            Character c = s.charAt(i);

            // number
            if (Character.isDigit(c)) cur = cur*10 + (c - '0');
            // operator || process the last digit
            if ((!Character.isDigit(c) && !Character.isWhitespace(c)) || (i == s.length() - 1)) {
                if (operator == '+' || operator == '-') {
                    res += last;
                    last = (operator == '+') ? cur : 0-cur;
                }
                else if (operator == '*') {
                    last *= cur;
                }
                else if (operator == '/') {
                    last /= cur;
                }

                operator = c;
                cur = 0;
            }
        }
        
        return (res + last);
    }
}