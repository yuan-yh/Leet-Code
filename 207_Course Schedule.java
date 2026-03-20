// Time complexity: O(V+E)
// Space complexity: O(V+E)
// V is the number of courses and E is the number of prerequisites.

class Solution {
    // Method 2: DFS
    private int[] visit;
    private Map<Integer, List<Integer>> prep;

    private boolean dfs(int course) {
        // 3. check for verified result || cycle
        if (this.visit[course] == 1) return false;
        if (this.visit[course] == 2) return true;
        
        // 4. update & check its prep
        this.visit[course] = 1;
        for (int i : this.prep.get(course)) {
            if (!dfs(i)) return false;
        }
        this.visit[course] = 2;
        return true;
    }

    public boolean canFinish(int numCourses, int[][] preq) {
        // 1. build prep list & visit array
        this.prep = new HashMap<>();
        for (int i = 0; i < numCourses; i++) this.prep.put(i, new ArrayList<>());

        for (int[] i : preq) this.prep.get(i[0]).add(i[1]);
        this.visit = new int[numCourses];

        // 2. check for cycle via DFS
        for (int i = 0; i < numCourses; i++) {
            if (!dfs(i)) return false;
        }
        return true;
    }

    // // Method 1: Topological Sort
    // // Time complexity: O(V+E)
    // // Space complexity: O(V+E)
    // // Where V is the number of courses and E is the numbe
    // public boolean canFinish(int numCourses, int[][] preq) {
    //     // 1. build adj list & record in-degree
    //     Map<Integer, List<Integer>> adj = new HashMap<>();
    //     for (int i = 0; i < numCourses; i++) adj.put(i, new ArrayList<>());
    //     int[] indegree = new int[numCourses];

    //     for (int[] i : preq) {
    //         int a = i[0], b = i[1];
    //         adj.get(b).add(a);
    //         indegree[a] += 1;
    //     }

    //     // 2. start from those w/n in-degree, check if we can finish all
    //     Deque<Integer> q = new LinkedList<>();
    //     for (int i = 0; i < numCourses; i++) {
    //         if (indegree[i] == 0) q.offer(i);
    //     }

    //     int cnt = 0;

    //     while (!q.isEmpty()) {
    //         int tmp =  q.poll();
    //         cnt += 1;
    //         List<Integer> tmpNext = adj.get(tmp);
    //         for (int i = 0; i < tmpNext.size(); i++) {
    //             int nextCourse = tmpNext.get(i);
    //             indegree[nextCourse] -= 1;
    //             if (indegree[nextCourse] == 0) q.offer(nextCourse);
    //         }
    //     }
    //     return cnt == numCourses;
    // }
}