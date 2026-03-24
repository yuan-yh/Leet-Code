// Time complexity: O(V+E)
// Space complexity: O(V+E)
// V is the number of courses and E is the number of prerequisites.

class Solution {
    // // Method 1. Topological Sort
    // public boolean canFinish(int numCourses, int[][] preq) {
    //     // 1. build adj-list & record in-degree
    //     Map<Integer, List<Integer>> cnext = new HashMap<>();
    //     int[] inDegree = new int[numCourses];

    //     for (int i = 0; i < numCourses; i++) cnext.put(i, new ArrayList<>());
    //     for (int[] i : preq) {
    //         cnext.get(i[1]).add(i[0]);
    //         inDegree[i[0]] += 1;
    //     }
        
    //     // 2. start from those w/n in-degree
    //     int cnt = 0;
    //     Deque<Integer> q = new LinkedList<>();
    //     for (int i = 0; i < numCourses; i++) {
    //         if (inDegree[i] == 0) q.offer(i);
    //     }

    //     while (!q.isEmpty()) {
    //         int tmp = q.poll();
    //         cnt += 1;
    //         for (int cn : cnext.get(tmp)) {
    //             inDegree[cn] -= 1;
    //             if (inDegree[cn] == 0) q.offer(cn);
    //         }
    //     }
    //     return cnt == numCourses;
    // }

    // Method 2. DFS - BT
    private Map<Integer, List<Integer>> cprev;
    private int[] visit;

    private boolean dfs(int course) {
        // 3. check for loop or verified results
        if (visit[course] == 1) return false;
        if (visit[course] == 2) return true;
        // 4. update the status & process its preq
        visit[course] = 1;
        for (int cp : cprev.get(course)) {
            if (!dfs(cp)) return false;
        }
        // 5. update to verified & return
        visit[course] = 2;
        return true;
    }

    public boolean canFinish(int numCourses, int[][] preq) {
        this.cprev = new HashMap<>();
        this.visit = new int[numCourses];

        // 1. build preq list for each course
        for (int i = 0; i < numCourses; i++) cprev.put(i, new ArrayList<>());
        for (int[] i : preq) cprev.get(i[0]).add(i[1]);

        // 2. loop - DFS to check each class
        for (int i = 0; i< numCourses; i++) {
            if (!dfs(i)) return false;
        }
        return true;
    }
}