// Time complexity: O(n)
// Space complexity:
// O(1) extra space, since we have at most 26 different characters.
// O(n) space for the output string.

class Solution {
    public String reorganizeString(String s) {
        // 1. count letter frequency
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) {
            count[s.charAt(i) - 'a'] ++;
        }
        // 2. push into PQ - int[]{count, letter}
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));
        for (int i = 0; i < count.length; i++) {
            if (count[i] > 0) pq.offer(new int[]{count[i], i});
        }
        // 3. repeatedly pick the most frequent letter
        StringBuilder sb = new StringBuilder();
        int[] prev = null;

        while (!pq.isEmpty() || prev != null) {
            if (pq.isEmpty() && prev != null) return "";

            int[] cur = pq.poll();
            sb.append((char) (cur[1] + 'a'));
            cur[0] --;

            if (prev != null) {
                pq.offer(prev);
                prev = null;
            }
            if (cur[0] > 0) prev = cur;
        }

        return sb.toString();
    }
}