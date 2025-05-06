// Time complexity: O(m⋅(n^2 * k − n*k^2))
// Space complexity: O(n)

class Solution {
    public String addBoldTag(String s, String[] words) {
        int sLength = s.length();
        boolean[] isBold = new boolean[sLength];

        // 1. locate words in s
        for (String w : words) {
            int start = s.indexOf(w);

            while (start != -1) {
                for (int i = start; i < (start + w.length()); i++) isBold[i] = true;
                start = s.indexOf(w, start+1);
            }
        }

        // 2. build res based on isBold
        StringBuilder sb = new StringBuilder();
        String openTag = "<b>";
        String closeTag = "</b>";
        for (int i = 0; i < sLength; i++) {
            // case - open tag: the cur char is bold & (no prev || prev is not bold)
            if (isBold[i] && (i == 0 || !isBold[i-1])) sb.append(openTag);
            sb.append(s.charAt(i));
            // case - close tag: the cur char is bold & (next is not bold || last char)
            if (isBold[i] && (i == sLength-1 || !isBold[i+1])) sb.append(closeTag);
        }
        return sb.toString();
    }
}