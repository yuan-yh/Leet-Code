// Time complexity: O(V+E)
// Space complexity: O(V+E)
// Where V is the number of courses and E is the number of prerequisites.

class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        int[] res = new int[numCourses];
        // 1. count inDegree & preq for each course
        int[] inDegree = new int[numCourses];
        Map<Integer, List<Integer>> next = new HashMap<>();

        for (int i = 0; i < numCourses; i++) next.put(i, new ArrayList<>());
        for (int[] p : prerequisites) {
            inDegree[p[0]] ++;
            next.get(p[1]).add(p[0]);
        }
        // 2. start with courses w/ no inDegree
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.add(i);
        }
        // 3. repeatedly record & eliminate courses w/ no inDegree, track with ptr to the index to be inserted in res
        int ptr = 0;
        while (!q.isEmpty()) {
            int curCourse = q.poll();
            res[ptr] = curCourse; 
            ptr ++;
            for (int c : next.get(curCourse)) {
                inDegree[c] --;
                if (inDegree[c] == 0) q.add(c);
            }
        }

        return (ptr == numCourses) ? res : new int[0];
    }
}