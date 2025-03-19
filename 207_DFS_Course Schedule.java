// Time complexity: O(V+E)
// Space complexity: O(V+E)
// V is the number of courses and E is the number of prerequisites.

class Solution {
    private Map<Integer, List<Integer>> preq;
    private Set<Integer> curPath;

    public boolean canFinish(int numCourses, int[][] prerequisites) {
        preq = new HashMap<>();
        curPath = new HashSet<>();

        // 1. record all preq for each course
        for (int i = 0; i < numCourses; i++) preq.put(i, new ArrayList<>());
        for (int[] p : prerequisites) preq.get(p[0]).add(p[1]);
        // 2. check each course
        for (int i = 0; i < numCourses; i++) {
            if (!dfs(i)) return false;
        }
        return true;
    }

    private boolean dfs(int course) {
        if (curPath.contains(course)) return false;

        curPath.add(course);
        for (int i : preq.get(course)) {
            if (!dfs(i)) return false;
        }
        preq.put(course, new ArrayList<>());
        curPath.remove(course);
        return true;
    }
}