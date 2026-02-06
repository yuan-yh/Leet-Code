class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # 二分图染色法
        nodes = len(graph)
        colors = [0] * nodes # 0 for unvisited, 1 for red, -1 for blue

        # 2. DFS - dye neighbors w/ diff colors
        def check(curNode: int, color: int) -> bool:
            # A. dye color
            colors[curNode] = color
            # B. explore neighbors (return if contradict; otherwise keep check)
            for n in graph[curNode]:
                if colors[n] == color or (colors[n] == 0 and not check(n, -color)):
                    return False
            return True
        
        # 1. loop the first unvisited node
        for n in range(nodes):
            if colors[n] == 0 and not check(n, 1):
                return False
        return True