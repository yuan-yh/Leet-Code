## Solution:
1. Calculate `distA[]` - distance from A to every node
2. Calculate `distB[]` - distance from B to every node  
3. Calculate `distToDest[]` - distance from Destination to every node
4. Loop through each node as a potential meeting point:
   - Calculate: `distA[node] + distB[node] + distToDest[node]`
   - Take the minimum

---

## Is this optimal? **Yes!**

### **时间复杂度分析：**
- 3 次 BFS：O(3 × (V + E)) = **O(V + E)**
- 遍历所有节点找最小值：O(V)
- **总时间复杂度：O(V + E)** ✅ 这是最优的

### **空间复杂度：**
- 3 个距离数组：**O(V)** ✅

### **为什么是最优的？**
因为：
1. 我们必须知道所有可能会合点的距离信息 → 必须遍历图
2. BFS 在无权图中找最短路径是最优的（O(V + E)）
3. 如果是带权图，用 Dijkstra 也是 O((V + E) log V)，仍然是最优的

### **无法更优化的原因：**
- 你不能只检查部分节点，因为最优会合点可能是图中的任何节点
- 你必须计算这 3 个距离数组，否则无法判断哪个会合点最优

---

## **Edge Cases to consider:**
1. **A 和 B 在同一位置** → 会合点就是起点
2. **目的地就是最优会合点** → A 和 B 各自直接去目的地
3. **图不连通** → 某些节点无法到达，距离为 ∞，需要处理
4. **多个最优会合点** → 需要返回所有最优会合点或任意一个

import heapq
from typing import List, Dict, Tuple

def shortestPathWithMeetingWeighted(graph: Dict[int, List[Tuple[int, int]]], 
                                   A: int, B: int, dest: int) -> float:
    """
    Find the shortest weighted path for A and B to meet and go to destination together.
    
    Args:
        graph: adjacency list with weights: {node: [(neighbor, weight), ...]}
        A: starting node for person A
        B: starting node for person B
        dest: destination node
    
    Returns:
        minimum total weighted distance
    """
    
    def dijkstra(start: int, graph: Dict[int, List[Tuple[int, int]]]) -> Dict[int, float]:
        """
        Dijkstra's algorithm to find shortest distance from start to all nodes.
        
        Returns:
            dictionary mapping node -> shortest distance from start
        """
        distances = {start: 0}
        # Min heap: (distance, node)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, node = heapq.heappop(pq)
            
            # Skip if already visited with better distance
            if node in visited:
                continue
            
            visited.add(node)
            
            # Visit all neighbors
            for neighbor, weight in graph.get(node, []):
                new_dist = current_dist + weight
                
                # Update if we found a shorter path
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return distances
    
    # Step 1: Dijkstra from A
    distA = dijkstra(A, graph)
    
    # Step 2: Dijkstra from B
    distB = dijkstra(B, graph)
    
    # Step 3: Dijkstra from destination
    distToDest = dijkstra(dest, graph)
    
    # Step 4: Find valid meeting points (reachable from A, B, and can reach dest)
    all_nodes = set(distA.keys()) & set(distB.keys()) & set(distToDest.keys())
    
    if not all_nodes:
        return -1  # No valid path exists
    
    # Step 5: Find minimum total weighted distance
    min_distance = float('inf')
    best_meeting_point = None
    
    for meeting_point in all_nodes:
        total_distance = (distA[meeting_point] + 
                         distB[meeting_point] + 
                         distToDest[meeting_point])
        
        if total_distance < min_distance:
            min_distance = total_distance
            best_meeting_point = meeting_point
    
    print(f"Best meeting point: {best_meeting_point}")
    return min_distance


# ============= 测试代码 =============

def test_weighted_example1():
    """
    测试加权图示例 1:
    Graph (weighted):
        A --5-- 1 --3-- 2 --2-- Dest
                |       |
                4       1
                |       |
                3 --2-- 4
                |
                1
                |
                B
    """
    graph = {
        'A': [(1, 5)],
        1: [('A', 5), (2, 3), (3, 4)],
        2: [(1, 3), (4, 1), ('Dest', 2)],
        3: [(1, 4), (4, 2), ('B', 1)],
        4: [(2, 1), (3, 2)],
        'B': [(3, 1)],
        'Dest': [(2, 2)]
    }
    
    result = shortestPathWithMeetingWeighted(graph, 'A', 'B', 'Dest')
    print(f"Example 1 - Minimum weighted distance: {result}")
    # Let's calculate:
    # Meet at 3: A->3: 9, B->3: 1, 3->Dest: 5, Total: 15
    # Meet at 4: A->3->4: 11, B->3->4: 3, 4->Dest: 3, Total: 17
    # Meet at 2: A->1->2: 8, B->3->4->2: 4, 2->Dest: 2, Total: 14


def test_weighted_example2():
    """
    测试加权图示例 2:
    A --10-- 1 --1-- Dest
             |
             5
             |
             B
    """
    graph = {
        'A': [(1, 10)],
        1: [('A', 10), ('Dest', 1), ('B', 5)],
        'B': [(1, 5)],
        'Dest': [(1, 1)]
    }
    
    result = shortestPathWithMeetingWeighted(graph, 'A', 'B', 'Dest')
    print(f"Example 2 - Minimum weighted distance: {result}")
    # Meet at 1: A->1: 10, B->1: 5, 1->Dest: 1, Total: 16


def test_weighted_example3():
    """
    测试加权图示例 3: Different weights make different meeting point optimal
    A --1-- M --1-- B
            |
            100
            |
            Dest
            
    vs if they each go directly:
    A --50-- Dest --50-- B
    """
    graph = {
        'A': [('M', 1), ('Dest', 50)],
        'M': [('A', 1), ('B', 1), ('Dest', 100)],
        'B': [('M', 1), ('Dest', 50)],
        'Dest': [('A', 50), ('B', 50), ('M', 100)]
    }
    
    result = shortestPathWithMeetingWeighted(graph, 'A', 'B', 'Dest')
    print(f"Example 3 - Minimum weighted distance: {result}")
    # Meet at M: A->M: 1, B->M: 1, M->Dest: 100, Total: 102
    # Meet at Dest: A->Dest: 50, B->Dest: 50, Dest->Dest: 0, Total: 100 ✓


# 运行测试
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Shortest Weighted Path with Meeting Point")
    print("=" * 60)
    test_weighted_example1()
    print()
    test_weighted_example2()
    print()
    test_weighted_example3()