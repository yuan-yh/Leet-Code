class Solution {
    public boolean validWordAbbreviation(String word, String abbr) {
        int w = 0, digit = 0;
        for (int a = 0; a < abbr.length(); a++) {
            Character ac = abbr.charAt(a);
            // case: letter (move w pointer -> compare)
            if (Character.isLetter(ac)) {
                w += digit;
                digit = 0;
                if (w >= word.length() || word.charAt(w) != abbr.charAt(a)) return false;
                w++;
            }
            // case: number (empty / leading zero)
            else {
                if (digit == 0 && (ac - '0') == 0) return false;
                digit = digit*10 + ac - '0';
            }
        }
        w += digit;
        return (w == word.length());
    }
}