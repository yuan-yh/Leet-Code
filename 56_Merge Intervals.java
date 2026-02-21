// 时间复杂度：O(nlogn)，其中 n 是 intervals 的长度。瓶颈在排序上。
// 空间复杂度：O(1)。排序的栈开销和返回值不计入。

class Solution {
    public int[][] merge(int[][] intervals) {
        // 1. sort by start time in ASC
        Arrays.sort(intervals, (a, b) -> (a[0] - b[0]));

        // 2. merge if curStart <= lastEnd, else add
        List<int[]> res = new ArrayList<>();

        for (int[] i : intervals) {
            int rSize = res.size();

            // case: add
            if (rSize == 0 || res.get(rSize-1)[1] < i[0]) res.add(i);
            // case: merge
            else res.get(rSize-1)[1] = Math.max(i[1], res.get(rSize-1)[1]);
        }

        return res.toArray(new int[res.size()][]);
    }
}