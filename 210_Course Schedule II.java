// Time complexity: O(V+E)
// Space complexity: O(V+E)
// Where V is the number of courses and E is the number of prerequisites.

class Solution {
    // // Method 1: topological sort
    // public int[] findOrder(int numCourses, int[][] preq) {
    //     // 1. build adj list & record in-degree
    //     Map<Integer, List<Integer>> adj = new HashMap<>();
    //     int[] indegree = new int[numCourses];

    //     for (int i = 0; i < numCourses; i++) adj.put(i, new ArrayList<>());

    //     for (int[] i : preq) {
    //         adj.get(i[1]).add(i[0]);
    //         indegree[i[0]] += 1;
    //     }

    //     // 2. start from those w/n in-degree
    //     Deque<Integer> q = new LinkedList<>();
    //     for (int i = 0; i < numCourses; i++) {
    //         if (indegree[i] == 0) q.offer(i);
    //     }

    //     List<Integer> path = new ArrayList<>();

    //     while (!q.isEmpty()) {
    //         int tmp = q.poll();
    //         path.add(tmp);

    //         for (int n : adj.get(tmp)) {
    //             indegree[n] -= 1;
    //             if (indegree[n] == 0) q.offer(n);
    //         }
    //     }
    //     return path.size() == numCourses ? path.stream().mapToInt(Integer::intValue).toArray() : new int[0];
    // }

    // Method 2: DFS
    private Map<Integer, List<Integer>> prep;
    private int[] visit;
    private List<Integer> path;

    private boolean dfs(int course) {
        // 3. check for cycle or verified result
        if (visit[course] == 1) return false;
        if (visit[course] == 2) return true;

        visit[course] = 1;
        // 4. check for preq then update
        for (int p : prep.get(course)) {
            if (!dfs(p)) return false;
        }
        path.add(course);
        visit[course] = 2;
        return true;
    }

    public int[] findOrder(int numCourses, int[][] preq) {
        // 1. build prep-list
        this.prep = new HashMap<>();
        this.visit = new int[numCourses];
        this.path = new ArrayList<>();

        for (int i = 0; i < numCourses; i++) prep.put(i, new ArrayList<>());
        for (int[] i : preq) prep.get(i[0]).add(i[1]);

        // 2. loop to check each course
        for (int i = 0; i < numCourses; i++) {
            if (!dfs(i)) return new int[0];
        }

        return this.path.stream().mapToInt(Integer::intValue).toArray();
    }
}