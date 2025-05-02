// Greedy (Max-Heap)
// Time complexity: O(n)
// Space complexity:O(1) extra space; O(n) space for the output string

class Solution {
    public String longestDiverseString(int a, int b, int c) {
        StringBuilder sb = new StringBuilder();
        // int[]{count, letter}
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> (y[0] - x[0]));

        // insert into the PQ
        if (a > 0) pq.offer(new int[]{a, 'a'});
        if (b > 0) pq.offer(new int[]{b, 'b'});
        if (c > 0) pq.offer(new int[]{c, 'c'});

        while (!pq.isEmpty()) {
            int[] first = pq.poll();

            // case: already exist the adjacent double-letter -> have to avoid 'first' now
            if (sb.length() > 1 && sb.charAt(sb.length() - 1) == first[1] && sb.charAt(sb.length() - 2) == first[1]) {
                // edge case: no one left other than 'first'
                if (pq.isEmpty()) break;

                int[] next = pq.poll();
                sb.append((char) next[1]);
                next[0] --;
                if (next[0] > 0) pq.offer(next);
                pq.offer(first);
            } else {
                sb.append((char) first[1]);
                first[0] --;
                if (first[0] > 0) pq.offer(first);
            }
        }

        return sb.toString();
    }
}