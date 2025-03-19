// Time complexity: O(V+E)
// Space complexity: O(V+E)
// Where V is the number of courses and E is the number of prerequisites.

class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        int[] inDegree = new int[numCourses];
        Map<Integer, List<Integer>> next = new HashMap<>();
        // 1. record preq for each course
        for (int i = 0; i < numCourses; i++) next.put(i, new ArrayList<>());
        for (int[] p : prerequisites) {
            inDegree[p[0]] ++;
            next.get(p[1]).add(p[0]);
        }
        // 2. find the course w/ no preq
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.add(i);
        }
        // 3. repeatedly complete courses w/ no preq
        int complete = 0;
        while (!q.isEmpty()) {
            int curCourse = q.poll();
            complete ++;
            for (int c : next.get(curCourse)) {
                inDegree[c] --;
                if (inDegree[c] == 0) q.add(c);
            }
        }
        return complete == numCourses;
    }
}