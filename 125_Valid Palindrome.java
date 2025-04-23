// Two Pointers
// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            // push leftwards
            while (left < right && !isAlphaNumeric(s.charAt(left))) left++;
            // push rightwards
            while (left < right && !isAlphaNumeric(s.charAt(right))) right--;
            // compare
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) return false;
            left++;
            right--;
        }
        return true;
    }

    private boolean isAlphaNumeric(Character c) {
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9')) return true;
        return false;
    }
}