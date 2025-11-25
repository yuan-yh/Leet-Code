## DLL
### Generic Type
```code
from typing import TypeVar, Generic, Optional, Any

T = TypeVar('T')  # Generic type variable

class ListNode(Generic[T]):
    def __init__(self, val: T):
        self.val: T = val
        self.next: Optional['ListNode[T]'] = None
        self.prev: Optional['ListNode[T]'] = None

class MyLinkedList(Generic[T]):
    def __init__(self):
        self.size = 0
        # Sentinel nodes - can use None since they're never accessed for value
        self.head: ListNode[Optional[T]] = ListNode(None)
        self.tail: ListNode[Optional[T]] = ListNode(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def get(self, index: int) -> Optional[T]:
        """
        Get the value of the index-th node in the linked list. 
        If the index is invalid, return None.
        """
        if index < 0 or index >= self.size:
            return None
        
        # Choose the fastest way: from head or tail
        if index + 1 < self.size - index:
            curr = self.head
            for _ in range(index + 1):
                curr = curr.next
        else:
            curr = self.tail
            for _ in range(self.size - index):
                curr = curr.prev
                
        return curr.val
            
    def addAtHead(self, val: T) -> None:
        """Add a node of value val before the first element."""
        pred, succ = self.head, self.head.next
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        
    def addAtTail(self, val: T) -> None:
        """Append a node of value val to the last element."""
        succ, pred = self.tail, self.tail.prev
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        
    def addAtIndex(self, index: int, val: T) -> None:
        """Add a node of value val before the index-th node."""
        if index > self.size:
            return
        
        if index < 0:
            index = 0
        
        # Find predecessor and successor
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev
        
        # Insertion
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        
    def deleteAtIndex(self, index: int) -> None:
        """Delete the index-th node if the index is valid."""
        if index < 0 or index >= self.size:
            return
        
        # Find predecessor and successor
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next.next
        else:
            succ = self.tail
            for _ in range(self.size - index - 1):
                succ = succ.prev
            pred = succ.prev.prev
            
        # Delete
        self.size -= 1
        pred.next = succ
        succ.prev = pred
    
    def __str__(self) -> str:
        """String representation of the list."""
        values = []
        curr = self.head.next
        while curr != self.tail:
            values.append(str(curr.val))
            curr = curr.next
        return " <-> ".join(values)
    
    def __len__(self) -> int:
        """Return the size of the list."""
        return self.size
```
```Testcase
# Integer list
int_list: MyLinkedList[int] = MyLinkedList()
int_list.addAtHead(1)
int_list.addAtTail(3)
print(int_list)  # 1 <-> 3

# String list
str_list: MyLinkedList[str] = MyLinkedList()
str_list.addAtHead("hello")
str_list.addAtTail("world")
print(str_list)  # hello <-> world

# Custom object list
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name}({self.age})"

person_list: MyLinkedList[Person] = MyLinkedList()
person_list.addAtHead(Person("Alice", 30))
person_list.addAtTail(Person("Bob", 25))
print(person_list)  # Alice(30) <-> Bob(25)

# Mixed type list (using Any)
mixed_list: MyLinkedList[Any] = MyLinkedList()
mixed_list.addAtHead(42)
mixed_list.addAtTail("text")
mixed_list.addAtTail([1, 2, 3])
```

### Common Implementation
```code
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next, self.prev = None, None

class MyLinkedList:
    def __init__(self):
        self.size = 0
        # sentinel nodes as pseudo-head and pseudo-tail
        self.head, self.tail = ListNode(0), ListNode(0) 
        self.head.next = self.tail
        self.tail.prev = self.head
        

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        # if index is invalid
        if index < 0 or index >= self.size:
            return -1
        
        # choose the fastest way: to move from the head
        # or to move from the tail
        if index + 1 < self.size - index:
            curr = self.head
            for _ in range(index + 1):
                curr = curr.next
        else:
            curr = self.tail
            for _ in range(self.size - index):
                curr = curr.prev
                
        return curr.val
            

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """
        pred, succ = self.head, self.head.next
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        succ, pred = self.tail, self.tail.prev
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """
        # If index is greater than the length, 
        # the node will not be inserted.
        if index > self.size:
            return
        
        # [so weird] If index is negative, 
        # the node will be inserted at the head of the list.
        if index < 0:
            index = 0
        
        # Find predecessor and successor of the node to be added
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev
        
        # Insertion itself
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        # If the index is invalid, do nothing
        if index < 0 or index >= self.size:
            return
        
        # Find the predecessor and successor of the node to be deleted
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next.next
        else:
            succ = self.tail
            for _ in range(self.size - index - 1):
                succ = succ.prev
            pred = succ.prev.prev
            
        # Delete pred.next 
        self.size -= 1
        pred.next = succ
        succ.prev = pred

<!-- Time complexity: O(1) for addAtHead and addAtTail. O(min(k,N−k)) for get, addAtIndex, and deleteAtIndex, where k is an index of the element to get, add or delete. -->
<!-- Space complexity: O(1) for all operations. -->
```

## Single-LL
```code
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class MyLinkedList:
    def __init__(self):
        self.size = 0
        self.head = ListNode(0)  # sentinel node as pseudo-head
        

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        # if index is invalid
        if index < 0 or index >= self.size:
            return -1
        
        curr = self.head
        # index steps needed 
        # to move from sentinel node to wanted index
        for _ in range(index + 1):
            curr = curr.next
        return curr.val
            

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """
        self.addAtIndex(0, val)
        

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        self.addAtIndex(self.size, val)
        

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """
        # If index is greater than the length, 
        # the node will not be inserted.
        if index > self.size:
            return
        
        # [so weird] If index is negative, 
        # the node will be inserted at the head of the list.
        if index < 0:
            index = 0
        
        self.size += 1
        # find predecessor of the node to be added
        pred = self.head
        for _ in range(index):
            pred = pred.next
            
        # node to be added
        to_add = ListNode(val)
        # insertion itself
        to_add.next = pred.next
        pred.next = to_add
        

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        # if the index is invalid, do nothing
        if index < 0 or index >= self.size:
            return
        
        self.size -= 1
        # find predecessor of the node to be deleted
        pred = self.head
        for _ in range(index):
            pred = pred.next
            
        # delete pred.next 
        pred.next = pred.next.next
```

## LRU
```code
class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dic = {}
        self.head = ListNode(-1, -1)
        self.tail = ListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.dic:
            return -1

        node = self.dic[key]
        self.remove(node)
        self.add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.dic:
            old_node = self.dic[key]
            self.remove(old_node)

        node = ListNode(key, value)
        self.dic[key] = node
        self.add(node)

        if len(self.dic) > self.capacity:
            node_to_delete = self.head.next
            self.remove(node_to_delete)
            del self.dic[node_to_delete.key]

    def add(self, node):
        previous_end = self.tail.prev
        previous_end.next = node
        node.prev = previous_end
        node.next = self.tail
        self.tail.prev = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

## LFU
```code
class LFUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.key2val = {}
        self.key2freq = {}
        self.freq2key = collections.defaultdict(collections.OrderedDict)
        self.minf = 0

    def get(self, key: int) -> int:
        if key not in self.key2val:
            return -1
        oldfreq = self.key2freq[key]
        self.key2freq[key] = oldfreq + 1
        self.freq2key[oldfreq].pop(key)
        if not self.freq2key[oldfreq]:
            del self.freq2key[oldfreq]
        self.freq2key[oldfreq + 1][key] = 1
        if self.minf not in self.freq2key:
            self.minf += 1
        return self.key2val[key]

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return
        if key in self.key2val:
            self.get(key)
            self.key2val[key] = value
            return

        if len(self.key2val) == self.cap:
            delkey, _ = self.freq2key[self.minf].popitem(last=False)
            del self.key2val[delkey]
            del self.key2freq[delkey]
        self.key2val[key] = value
        self.key2freq[key] = 1
        self.freq2key[1][key] = 1
        self.minf = 1
```

## Course Schedule Order
```code
# BFS: root (no-prep course) -> leaf, so record adj_next
# DFS: leaf -> root, so record adj_prev

# Method 2: BFS
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # check from root to leafnode, so use adj_next
        # 1. build adj_next & prep array
        adj_next = [[] for _ in range(numCourses)]
        prep = [0] * numCourses        

        for n, p in prerequisites:
            adj_next[p].append(n)
            prep[n] += 1
        
        # 2. enque all non-prep courses
        q = deque()
        for i, p in enumerate(prep):
            if p == 0:
                q.append(i)
        
        # 3. pop -> process its next by prep -=1 -> process once no prep
        res = []

        while q:
            cur = q.popleft()
            res.append(cur)

            for n in adj_next[cur]:
                prep[n] -= 1
                if prep[n] == 0:
                    q.append(n)
        return res if len(res) == numCourses else []

# # Method 1: DFS
# class Solution:
#     def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
#         # from leafnode to root, so build an adj_prev array and a visit status array to detect cycle
#         adj_prep = [[] for _ in range(numCourses)]
#         visit = [0] * numCourses

#         for n, p in prerequisites:
#             adj_prep[n].append(p)
        
#         # hasCycle function: process prep first, then append the cur course
#         def hasCycle(course: int) -> bool:
#             # 1. check for end case: visiting in cycle or complete
#             if visit[course] == 1:
#                 return True
#             if visit[course] == 2:
#                 return False
#             # 2. update and process prep
#             visit[course] = 1
#             for p in adj_prep[course]:
#                 if hasCycle(p):
#                     return True
#             # 3. update and append
#             visit[course] = 2
#             res.append(course)
#             return False
        
#         res = []

#         for i in range(numCourses):
#             if hasCycle(i):
#                 return []
#         return res

```

## Meeting Room Number
```code
class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # 1. sort intervals
        intervals.sort(key = lambda x : (x[0], x[1]))
        # 2. heap: release all rooms before start, then push end time
        room = []
        res = 0
        for start, end in intervals:
            while room and room[0] <= start:
                heappop(room)
            heappush(room, end)
            res = max(res, len(room))
        return res
```

## 二叉树
### 二叉树 -> 不同形状的岛屿数量
```code
from collections import deque, defaultdict
from typing import Optional, List, Set, Tuple

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def numDistinctIslandsInBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        在二叉树中找出不同形状的岛屿数量
        
        相邻定义：
        1. 同一层的左右相邻节点
        2. 父子关系的节点
        """
        if not root:
            return 0
        
        # Step 1: 将二叉树转换为2D网格表示
        grid, node_positions = self.treeToGrid(root)
        
        if not grid:
            return 0
        
        # Step 2: 在网格中找出不同的岛屿形状
        return self.countDistinctIslands(grid)
    
    def treeToGrid(self, root: Optional[TreeNode]) -> Tuple[List[List[int]], dict]:
        """
        将二叉树转换为2D网格
        返回：(grid, node_positions)
        grid[level][position] = node.val
        """
        if not root:
            return [], {}
        
        # BFS遍历，记录每个节点的层级和水平位置
        queue = deque([(root, 0, 0)])  # (node, level, position)
        levels = defaultdict(dict)  # {level: {position: value}}
        min_pos, max_pos = 0, 0
        max_level = 0
        
        while queue:
            node, level, pos = queue.popleft()
            
            if node:
                levels[level][pos] = node.val
                min_pos = min(min_pos, pos)
                max_pos = max(max_pos, pos)
                max_level = max(max_level, level)
                
                queue.append((node.left, level + 1, pos * 2))
                queue.append((node.right, level + 1, pos * 2 + 1))
        
        # 构建网格
        width = max_pos - min_pos + 1
        height = max_level + 1
        grid = [[0] * width for _ in range(height)]
        node_positions = {}  # 记录节点在网格中的位置
        
        for level in range(height):
            for pos, val in levels[level].items():
                grid_col = pos - min_pos
                grid[level][grid_col] = val
                node_positions[(level, pos)] = (level, grid_col)
        
        return grid, node_positions
    
    def countDistinctIslands(self, grid: List[List[int]]) -> int:
        """
        在2D网格中计算不同形状的岛屿数量
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        visited = set()
        unique_shapes = set()
        
        def dfs(r, c, r0, c0, path):
            """DFS遍历岛屿并记录形状"""
            if (r < 0 or r >= m or c < 0 or c >= n or 
                grid[r][c] == 0 or (r, c) in visited):
                return
            
            visited.add((r, c))
            # 记录相对位置
            path.append((r - r0, c - c0))
            
            # 四方向探索
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(r + dr, c + dc, r0, c0, path)
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and (i, j) not in visited:
                    path = []
                    dfs(i, j, i, j, path)
                    if path:  # 确保路径非空
                        unique_shapes.add(tuple(path))
        
        return len(unique_shapes)
    
    def numDistinctIslandsInBinaryTreeAdvanced(self, root: Optional[TreeNode]) -> int:
        """
        高级版本：直接在树结构上工作，考虑树的特殊相邻关系
        
        相邻定义：
        1. 父子节点
        2. 兄弟节点（同一父节点的左右子节点）
        """
        if not root:
            return 0
        
        # 构建树的邻接关系
        adjacency = defaultdict(set)
        node_map = {}  # id -> TreeNode
        node_id = {}  # TreeNode -> id
        id_counter = [0]
        
        def build_adjacency(node, parent=None):
            if not node:
                return None
            
            # 分配唯一ID
            curr_id = id_counter[0]
            id_counter[0] += 1
            node_id[node] = curr_id
            node_map[curr_id] = node
            
            # 父子关系
            if parent is not None and node.val == 1 and parent.val == 1:
                adjacency[node_id[parent]].add(curr_id)
                adjacency[curr_id].add(node_id[parent])
            
            left_id = build_adjacency(node.left, node)
            right_id = build_adjacency(node.right, node)
            
            # 兄弟关系
            if (left_id is not None and right_id is not None and 
                node_map[left_id].val == 1 and node_map[right_id].val == 1):
                adjacency[left_id].add(right_id)
                adjacency[right_id].add(left_id)
            
            return curr_id
        
        build_adjacency(root)
        
        # DFS找岛屿
        visited = set()
        unique_shapes = set()
        
        def dfs_island(node_id, start_id, path):
            if node_id in visited or node_map[node_id].val == 0:
                return
            
            visited.add(node_id)
            # 记录相对于起点的"位置"（这里用ID差值模拟）
            path.append(node_id - start_id)
            
            for neighbor in adjacency[node_id]:
                if neighbor not in visited and node_map[neighbor].val == 1:
                    dfs_island(neighbor, start_id, path)
        
        for nid in node_map:
            if nid not in visited and node_map[nid].val == 1:
                path = []
                dfs_island(nid, nid, path)
                if path:
                    # 排序以确保相同形状有相同表示
                    path.sort()
                    unique_shapes.add(tuple(path))
        
        return len(unique_shapes)


# 测试代码
def test_solution():
    # 构建测试树
    #       1
    #      / \
    #     1   0
    #    / \
    #   1   1
    root1 = TreeNode(1)
    root1.left = TreeNode(1)
    root1.right = TreeNode(0)
    root1.left.left = TreeNode(1)
    root1.left.right = TreeNode(1)
    
    solution = Solution()
    
    # 测试基本方法
    print("测试用例1:")
    result = solution.numDistinctIslandsInBinaryTree(root1)
    print(f"不同岛屿数量: {result}")
    
    # 构建另一个测试树
    #       1
    #      / \
    #     1   1
    #    /     \
    #   0       1
    root2 = TreeNode(1)
    root2.left = TreeNode(1)
    root2.right = TreeNode(1)
    root2.left.left = TreeNode(0)
    root2.right.right = TreeNode(1)
    
    print("\n测试用例2:")
    result = solution.numDistinctIslandsInBinaryTree(root2)
    print(f"不同岛屿数量: {result}")
    
    # 显示网格表示
    grid1, _ = solution.treeToGrid(root1)
    print("\n树1的网格表示:")
    for row in grid1:
        print(row)
    
    grid2, _ = solution.treeToGrid(root2)
    print("\n树2的网格表示:")
    for row in grid2:
        print(row)


if __name__ == "__main__":
    test_solution()
```

### 二叉树 <- Directed Graph
edge case: multiple-or-no roots / cycle / self-loop / in-degree > 1

```code
from collections import defaultdict, deque
from typing import List, Tuple, Optional, Set

# Method 1: BFS
class TreeValidator:
    def isValidTree(self, n: int, edges: List[List[int]]) -> bool:
        """
        验证有向图是否构成树
        
        Args:
            n: 节点数量 (节点编号从0到n-1)
            edges: 边的列表，每条边是[from, to]
        
        Returns:
            bool: 是否构成有效的树
        """
        # 边界情况1：空图
        if n == 0:
            return True
        
        # 边界情况2：单个节点
        if n == 1:
            return len(edges) == 0
        
        # 边界情况3：树需要恰好n-1条边
        if len(edges) != n - 1:
            return False
        
        # 构建邻接表和计算入度
        graph = defaultdict(list)
        in_degree = [0] * n
        
        for from_node, to_node in edges:
            # 边界情况4：检查节点是否有效
            if from_node >= n or to_node >= n or from_node < 0 or to_node < 0:
                return False
            
            # 边界情况5：自环
            if from_node == to_node:
                return False
            
            graph[from_node].append(to_node)
            in_degree[to_node] += 1
        
        # 找根节点（入度为0的节点）
        roots = [i for i in range(n) if in_degree[i] == 0]
        
        # 必须恰好有一个根节点
        if len(roots) != 1:
            return False
        
        root = roots[0]
        
        # 检查所有非根节点的入度是否为1
        for i in range(n):
            if i != root and in_degree[i] != 1:
                return False
        
        # 检查是否有环以及连通性（使用BFS）
        visited = set()
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            if node in visited:
                # 发现环
                return False
            
            visited.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
        
        # 检查是否所有节点都被访问（连通性）
        return len(visited) == n

# Method 2: DFS
    def isValidTreeDFS(self, n: int, edges: List[List[int]]) -> bool:
        """
        使用DFS的替代实现
        """
        if n == 0:
            return True
        if n == 1:
            return len(edges) == 0
        if len(edges) != n - 1:
            return False
        
        graph = defaultdict(list)
        in_degree = [0] * n
        
        for from_node, to_node in edges:
            if from_node >= n or to_node >= n or from_node < 0 or to_node < 0:
                return False
            if from_node == to_node:
                return False
            
            graph[from_node].append(to_node)
            in_degree[to_node] += 1
        
        # 找根节点
        roots = [i for i in range(n) if in_degree[i] == 0]
        if len(roots) != 1:
            return False
        
        root = roots[0]
        
        # DFS检查环和连通性
        visited = set()
        rec_stack = set()  # 递归栈，用于检测环
        
        def dfs(node: int) -> bool:
            if node in rec_stack:
                # 在当前路径中再次访问，说明有环
                return False
            
            if node in visited:
                # 已经访问过但不在当前路径中，跳过
                return True
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            
            rec_stack.remove(node)
            return True
        
        # 从根节点开始DFS
        if not dfs(root):
            return False
        
        # 检查是否所有节点都被访问
        return len(visited) == n

# Method 3: 并查集
    def isValidTreeUnionFind(self, n: int, edges: List[List[int]]) -> bool:
        """
        使用并查集的实现（适用于无向图，这里仅作参考）
        """
        if n == 0:
            return True
        if len(edges) != n - 1:
            return False
        
        parent = list(range(n))
        
        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x: int, y: int) -> bool:
            root_x = find(x)
            root_y = find(y)
            
            if root_x == root_y:
                return False  # 已经在同一集合中，添加边会形成环
            
            parent[root_x] = root_y
            return True
        
        for from_node, to_node in edges:
            if not union(from_node, to_node):
                return False
        
        # 检查是否所有节点都连通
        root = find(0)
        return all(find(i) == root for i in range(n))

class TreeValidatorWithDuplicateEdges:
    """处理可能有重复边的情况"""
    
    def isValidTree(self, n: int, edges: List[List[int]]) -> bool:
        if n == 0:
            return True
        if n == 1:
            return len(edges) == 0
        
        # 使用集合去重
        unique_edges = set()
        graph = defaultdict(set)  # 使用set避免重复
        in_degree = defaultdict(int)
        
        for from_node, to_node in edges:
            # 检查有效性
            if from_node >= n or to_node >= n or from_node < 0 or to_node < 0:
                return False
            if from_node == to_node:
                return False
            
            # 检查重复边
            edge = (from_node, to_node)
            if edge in unique_edges:
                return False  # 有重复边，不是树
            
            unique_edges.add(edge)
            graph[from_node].add(to_node)
            in_degree[to_node] += 1
        
        # 树必须有n-1条边
        if len(unique_edges) != n - 1:
            return False
        
        # 后续验证逻辑相同...
        roots = [i for i in range(n) if in_degree[i] == 0]
        if len(roots) != 1:
            return False
        
        # BFS验证
        visited = set()
        queue = deque([roots[0]])
        
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return len(visited) == n


# 测试代码
def test_tree_validator():
    validator = TreeValidator()
    
    # 测试用例1：有效的树
    print("测试用例1 - 有效的树:")
    n = 4
    edges = [[0, 1], [0, 2], [0, 3]]
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # True
    print()
    
    # 测试用例2：有环
    print("测试用例2 - 有环:")
    n = 4
    edges = [[0, 1], [1, 2], [2, 0], [0, 3]]
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # False
    print()
    
    # 测试用例3：不连通（森林）
    print("测试用例3 - 不连通:")
    n = 4
    edges = [[0, 1], [2, 3]]
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # False
    print()
    
    # 测试用例4：多个根
    print("测试用例4 - 多个根:")
    n = 4
    edges = [[0, 1], [2, 3]]
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # False
    print()
    
    # 测试用例5：空图
    print("测试用例5 - 空图:")
    n = 0
    edges = []
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # True
    print()
    
    # 测试用例6：单个节点
    print("测试用例6 - 单个节点:")
    n = 1
    edges = []
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # True
    print()
    
    # 测试用例7：自环
    print("测试用例7 - 自环:")
    n = 2
    edges = [[0, 0]]
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # False
    print()
    
    # 测试用例8：节点入度大于1
    print("测试用例8 - 节点入度大于1:")
    n = 3
    edges = [[0, 1], [2, 1]]
    print(f"n={n}, edges={edges}")
    print(f"结果: {validator.isValidTree(n, edges)}")  # False

if __name__ == "__main__":
    test_tree_validator()
```

## Person & Apartment
步骤1：按偏好分类人员 -> 步骤2：按房间数分类公寓 -> 步骤3：优先处理想独居的人 -> 步骤4：处理想合租的人

步骤5：处理剩余想合租的人（妥协方案） -> 步骤6：处理剩余想独居的人（妥协方案） -> 步骤7：找出未分配的人
```code
class Person:
    def __init__(self, name, wants_share):
        self.name = name
        self.wants_share = wants_share

class Apartment:
    def __init__(self, apt_num, num_rooms):
        self.apt_num = apt_num
        self.num_rooms = num_rooms

def assign_apartments(people, apartments):
    """
    Assign apartments to people based on their sharing preference
    Returns:
    - apartment_assignments: dict {apt_num: [person_names]}
    - unassigned: list of unassigned person names
    """
    from collections import defaultdict
    
    # Step 1: Separate people by preference
    want_share = [p for p in people if p.wants_share]
    want_alone = [p for p in people if not p.wants_share]
    
    # Step 2: Separate apartments by room count
    single_rooms = [apt for apt in apartments if apt.num_rooms == 1]
    multi_rooms = [apt for apt in apartments if apt.num_rooms > 1]
    
    # Use defaultdict to group people by apartment
    apartment_assignments = defaultdict(list)
    
    # Track how many spaces are left in each multi-room apartment
    multi_room_spaces = {}  # {apt_num: remaining_spaces}
    
    # Step 3: Assign people who want to be alone to single rooms FIRST
    for person in want_alone:
        if single_rooms:
            apt = single_rooms.pop(0)
            apartment_assignments[apt.apt_num].append(person.name)
        else:
            # No single rooms, we'll handle them later
            pass
    
    # Step 4: Assign people who want to share to multi-rooms
    i = 0
    while i < len(want_share):
        if multi_rooms:
            apt = multi_rooms.pop(0)
            spaces = apt.num_rooms
            # Assign multiple people to this apartment 将多个人分配到这个公寓
            for _ in range(min(spaces, len(want_share) - i)):
                apartment_assignments[apt.apt_num].append(want_share[i].name)
                i += 1
                spaces -= 1
            # Track remaining spaces in this apartment 记录剩余空间
            if spaces > 0:
                multi_room_spaces[apt.apt_num] = spaces
        else:
            # No multi-rooms left, we'll handle them later
            break
    
    # Step 5: Handle remaining want_share people (violate preference)
    while i < len(want_share):
        if single_rooms:
            apt = single_rooms.pop(0)
            apartment_assignments[apt.apt_num].append(want_share[i].name)
            i += 1
        else:
            break
    
    # Step 6: Handle remaining want_alone people
    # First try to use leftover spaces in multi-rooms
    for person in want_alone:
        if person.name not in [name for names in apartment_assignments.values() for name in names]:
            # Check if there are empty spaces in multi-room apartments
            if multi_room_spaces:
                # Get an apartment with available space
                apt_num = next(iter(multi_room_spaces))
                apartment_assignments[apt_num].append(person.name)
                multi_room_spaces[apt_num] -= 1
                if multi_room_spaces[apt_num] == 0:
                    del multi_room_spaces[apt_num]
            else:
                # No space anywhere
                break
    
    # Step 7: Find unassigned people
    assigned_names = set()
    for people_list in apartment_assignments.values():
        assigned_names.update(people_list)
    
    unassigned = [p.name for p in people if p.name not in assigned_names]
    
    # Convert defaultdict to regular dict for cleaner output
    return dict(apartment_assignments), unassigned

# Example usage
people = [
    Person("Alice", False),
    Person("Bob", True),
    Person("Charlie", True),
    Person("David", False),
    Person("Eve", False),
    Person("Jason", False)
]

apartments = [
    Apartment(101, 1),
    Apartment(102, 1),
    Apartment(103, 1),
    Apartment(104, 3)
]

apartment_assignments, unassigned = assign_apartments(people, apartments)

print("Apartment Assignments:")
for apt_num, residents in apartment_assignments.items():
    print(f"  Apartment {apt_num}: {', '.join(residents)}")

print(f"\nUnassigned: {unassigned}")

### Output:
# ```
# Apartment Assignments:
#   Apartment 101: {Alice}
#   Apartment 102: {David}
#   Apartment 103: {Eve}
#   Apartment 104: {Bob, Charlie, Jason}
# 
# Unassigned: []
```

## 餐厅waitlist -加/删/serve客人
edge case: 重复加入：检查 waiting_parties 和 served_parties; 重复离开：检查是否在等候名单中; 无效参数：空ID、负数人数等; 空队列：服务客人时队列为空; 已服务重新加入：防止使用相同ID

假设: 桌子容量固定：每张桌子有固定座位数，不能拼桌; 严格匹配：只有当桌子容量与客人数量完全匹配时才能serve; 先到先得：同样大小的团体按照加入顺序服务（FIFO）; 唯一标识：每个客人团体有唯一ID（如电话号码或姓名）; 防重复操作：同一团体不能重复加入或离开

waitlist_by_size：使用 defaultdict(deque), 按团体大小分组，每组是一个FIFO队列, O(1) 的入队和出队操作

waiting_parties：使用字典, 快速查找某个团体是否在等候, O(1) 的查找时间

served_parties：使用集合, 防止已服务的客人重新加入, O(1) 的查找时间
```code
from collections import deque, defaultdict
from typing import Dict, Set, Optional, List, Tuple
from datetime import datetime

class Party:
    """代表一个客人团体"""
    def __init__(self, party_id: str, size: int, name: str = ""):
        self.party_id = party_id
        self.size = size
        self.name = name
        self.join_time = datetime.now()
    
    def __repr__(self):
        return f"Party({self.party_id}, size={self.size}, name={self.name})"

class RestaurantWaitlist:
    """餐厅等候名单管理系统"""
    
    def __init__(self):
        # 按团体大小分组的等候队列
        # {party_size: deque([party1, party2, ...])}
        self.waitlist_by_size = defaultdict(deque)
        
        # 记录当前在等候名单中的所有party_id
        # {party_id: Party对象}
        self.waiting_parties = {}
        
        # 已服务的客人（防止重复操作）
        self.served_parties = set()
        
        # 统计信息
        self.stats = {
            'total_joined': 0,
            'total_served': 0,
            'total_left': 0,
            'current_waiting': 0
        }
    
    def join_waitlist(self, party_id: str, size: int, name: str = "") -> Tuple[bool, str]:
        """
        将客人团体加入等候名单
        
        Args:
            party_id: 团体唯一标识（如电话号码）
            size: 团体人数
            name: 团体名称（可选）
        
        Returns:
            (成功与否, 消息)
        """
        # 边界检查1：检查参数有效性
        if not party_id or size <= 0:
            return False, "无效的参数：ID不能为空，人数必须大于0"
        
        # 边界检查2：检查是否已在等候名单中
        if party_id in self.waiting_parties:
            existing = self.waiting_parties[party_id]
            return False, f"团体 {party_id} 已在等候名单中（人数：{existing.size}）"
        
        # 边界检查3：检查是否已经被服务过（防止已服务的客人重新加入）
        if party_id in self.served_parties:
            return False, f"团体 {party_id} 已经被服务过，请使用新的ID"
        
        # 创建新的Party对象
        party = Party(party_id, size, name)
        
        # 加入对应大小的等候队列
        self.waitlist_by_size[size].append(party)
        
        # 记录到总的等候名单中
        self.waiting_parties[party_id] = party
        
        # 更新统计
        self.stats['total_joined'] += 1
        self.stats['current_waiting'] += 1
        
        # 获取当前排队位置
        position = len(self.waitlist_by_size[size])
        
        return True, f"成功加入等候名单。团体 {party_id}（{size}人）当前在{size}人桌队列的第{position}位"
    
    def leave_waitlist(self, party_id: str) -> Tuple[bool, str]:
        """
        客人离开等候名单
        
        Args:
            party_id: 团体唯一标识
        
        Returns:
            (成功与否, 消息)
        """
        # 边界检查1：检查参数有效性
        if not party_id:
            return False, "无效的参数：ID不能为空"
        
        # 边界检查2：检查是否在等候名单中
        if party_id not in self.waiting_parties:
            # 检查是否已经被服务
            if party_id in self.served_parties:
                return False, f"团体 {party_id} 已经被服务，不在等候名单中"
            return False, f"团体 {party_id} 不在等候名单中"
        
        # 获取Party对象
        party = self.waiting_parties[party_id]
        size = party.size
        
        # 从对应大小的队列中移除
        # 注意：这里需要遍历队列找到并移除，因为可能不在队首
        waitlist = self.waitlist_by_size[size]
        
        # 创建新队列，不包含要离开的party
        new_queue = deque()
        removed = False
        
        while waitlist:
            current = waitlist.popleft()
            if current.party_id == party_id:
                removed = True
            else:
                new_queue.append(current)
        
        self.waitlist_by_size[size] = new_queue
        
        if not removed:
            return False, f"内部错误：无法从队列中移除团体 {party_id}"
        
        # 从总名单中移除
        del self.waiting_parties[party_id]
        
        # 如果该大小的队列为空，删除该键
        if not self.waitlist_by_size[size]:
            del self.waitlist_by_size[size]
        
        # 更新统计
        self.stats['total_left'] += 1
        self.stats['current_waiting'] -= 1
        
        wait_time = (datetime.now() - party.join_time).seconds // 60
        
        return True, f"团体 {party_id}（{size}人）已离开等候名单，等候时间：{wait_time}分钟"
    
    def serve_customers(self, table_size: int) -> Tuple[bool, str, Optional[Party]]:
        """
        当有空桌子时服务客人
        
        Args:
            table_size: 可用桌子的座位数
        
        Returns:
            (成功与否, 消息, 被服务的Party对象)
        """
        # 边界检查：桌子大小有效性
        if table_size <= 0:
            return False, "无效的桌子大小", None
        
        # 检查是否有匹配大小的等候团体
        if table_size not in self.waitlist_by_size or not self.waitlist_by_size[table_size]:
            sizes = list(self.waitlist_by_size.keys())
            if sizes:
                return False, f"没有{table_size}人的团体在等候。当前等候的团体大小：{sorted(sizes)}", None
            else:
                return False, "等候名单为空", None
        
        # 获取队首的团体（FIFO）
        party = self.waitlist_by_size[table_size].popleft()
        
        # 从总名单中移除
        del self.waiting_parties[party.party_id]
        
        # 加入已服务名单
        self.served_parties.add(party.party_id)
        
        # 如果该大小的队列为空，删除该键
        if not self.waitlist_by_size[table_size]:
            del self.waitlist_by_size[table_size]
        
        # 更新统计
        self.stats['total_served'] += 1
        self.stats['current_waiting'] -= 1
        
        # 计算等候时间
        wait_time = (datetime.now() - party.join_time).seconds // 60
        
        return True, f"成功服务团体 {party.party_id}（{party.size}人），等候时间：{wait_time}分钟", party
    
    def get_waitlist_status(self) -> Dict:
        """获取当前等候名单状态"""
        status = {
            'summary': self.stats.copy(),
            'by_size': {}
        }
        
        for size, queue in self.waitlist_by_size.items():
            status['by_size'][size] = [
                {
                    'party_id': party.party_id,
                    'name': party.name,
                    'wait_time_minutes': (datetime.now() - party.join_time).seconds // 60
                }
                for party in queue
            ]
        
        return status
    
    def get_next_party(self, table_size: int) -> Optional[Party]:
        """查看（但不移除）下一个要被服务的团体"""
        if table_size in self.waitlist_by_size and self.waitlist_by_size[table_size]:
            return self.waitlist_by_size[table_size][0]
        return None
    
    def estimate_wait_time(self, party_id: str, avg_dining_minutes: int = 60) -> Optional[int]:
        """
        估算等候时间
        
        Args:
            party_id: 团体ID
            avg_dining_minutes: 平均用餐时间（分钟）
        
        Returns:
            估算的等候时间（分钟）
        """
        if party_id not in self.waiting_parties:
            return None
        
        party = self.waiting_parties[party_id]
        queue = self.waitlist_by_size[party.size]
        
        # 找到在队列中的位置
        position = 0
        for p in queue:
            if p.party_id == party_id:
                break
            position += 1
        
        # 估算等候时间 = 位置 × 平均用餐时间
        return position * avg_dining_minutes


# 使用示例和测试
def test_restaurant_waitlist():
    print("=== 餐厅等候名单系统测试 ===\n")
    
    waitlist = RestaurantWaitlist()
    
    # 测试1：正常加入
    print("测试1：正常加入等候名单")
    success, msg = waitlist.join_waitlist("alice_123", 2, "Alice")
    print(f"  {msg}")
    
    success, msg = waitlist.join_waitlist("bob_456", 4, "Bob")
    print(f"  {msg}")
    
    success, msg = waitlist.join_waitlist("charlie_789", 2, "Charlie")
    print(f"  {msg}")
    
    success, msg = waitlist.join_waitlist("david_012", 4, "David")
    print(f"  {msg}")
    
    # 测试2：重复加入
    print("\n测试2：防止重复加入")
    success, msg = waitlist.join_waitlist("alice_123", 2, "Alice")
    print(f"  {msg}")
    
    # 测试3：无效参数
    print("\n测试3：无效参数检查")
    success, msg = waitlist.join_waitlist("", 2)
    print(f"  {msg}")
    
    success, msg = waitlist.join_waitlist("test", -1)
    print(f"  {msg}")
    
    # 测试4：查看状态
    print("\n测试4：当前等候状态")
    status = waitlist.get_waitlist_status()
    print(f"  总计加入：{status['summary']['total_joined']}")
    print(f"  当前等候：{status['summary']['current_waiting']}")
    for size, parties in status['by_size'].items():
        print(f"  {size}人桌：{len(parties)}组等候")
        for p in parties:
            print(f"    - {p['party_id']} ({p['name']})")
    
    # 测试5：服务客人
    print("\n测试5：服务客人")
    success, msg, party = waitlist.serve_customers(2)
    print(f"  {msg}")
    
    success, msg, party = waitlist.serve_customers(3)
    print(f"  {msg}")
    
    # 测试6：客人离开
    print("\n测试6：客人主动离开")
    success, msg = waitlist.leave_waitlist("david_012")
    print(f"  {msg}")
    
    # 测试7：重复离开
    print("\n测试7：防止重复离开")
    success, msg = waitlist.leave_waitlist("david_012")
    print(f"  {msg}")
    
    # 测试8：已服务的客人不能重新加入
    print("\n测试8：已服务客人不能重新加入")
    success, msg = waitlist.join_waitlist("alice_123", 2)
    print(f"  {msg}")
    
    # 测试9：估算等候时间
    print("\n测试9：估算等候时间")
    wait_time = waitlist.estimate_wait_time("charlie_789", 45)
    print(f"  Charlie的估算等候时间：{wait_time}分钟")
    
    # 最终状态
    print("\n最终统计：")
    status = waitlist.get_waitlist_status()
    print(f"  总计加入：{status['summary']['total_joined']}")
    print(f"  总计服务：{status['summary']['total_served']}")
    print(f"  主动离开：{status['summary']['total_left']}")
    print(f"  当前等候：{status['summary']['current_waiting']}")

if __name__ == "__main__":
    test_restaurant_waitlist()
```

## Encode & Decode
```code
class Codec:
    def encode(self, strs):
        # Initialize an empty string to hold the encoded string.
        encoded_string = ''
        for s in strs:
            # Append the length, the delimiter, and the string itself.
            encoded_string += str(len(s)) + '/:' + s
        return encoded_string

    def decode(self, s):
        # Initialize a list to hold the decoded strings.
        decoded_strings = []
        i = 0
        while i < len(s):
            # Find the delimiter.
            delim = s.find('/:', i)
            # Get the length, which is before the delimiter.
            length = int(s[i:delim])
            # Get the string, which is of 'length' length after the delimiter.
            str_ = s[delim+2 : delim+2+length]
            # Add the string to the list.
            decoded_strings.append(str_)
            # Move the index to the start of the next length.
            i = delim + 2 + length
        return decoded_strings

<!-- Time Complexity: O(n), Space Complexity: O(k). -->
```

## 字典拼单词
```code
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # 优化1：找出字典中最长单词的长度，用于剪枝
        max_len = max(map(len, wordDict))
        
        # 优化2：将列表转换为集合，O(1)时间复杂度查找
        words = set(wordDict)
        
        @cache  # Python 3.9+ 的缓存装饰器，实现记忆化
        def dfs(i: int) -> bool:
            """
            判断s[0:i]是否可以被拆分
            i 表示当前要检查的字符串末尾位置（不包含）
            """
            # 基础情况：空字符串，表示成功拆分完毕
            if i == 0:
                return True
            
            # 尝试所有可能的拆分点j
            # s[j:i] 是我们要检查的单词
            for j in range(i - 1, max(i - max_len - 1, -1), -1):
                # 检查两个条件：
                # 1. s[j:i] 在字典中
                # 2. s[0:j] 可以被成功拆分（递归调用）
                if s[j:i] in words and dfs(j):
                    return True
            
            return False
        
        # 从整个字符串开始
        return dfs(len(s))
```

以 `s = "leetcode"`, `wordDict = ["leet", "code"]` 为例：
```
初始调用: dfs(8) - 检查 s[0:8] = "leetcode"

dfs(8):
  j=7: s[7:8]="e"     ❌ 不在字典中
  j=6: s[6:8]="de"    ❌ 不在字典中
  j=5: s[5:8]="ode"   ❌ 不在字典中
  j=4: s[4:8]="code"  ✅ 在字典中！
       → 递归调用 dfs(4)
       
dfs(4): 检查 s[0:4] = "leet"
  j=3: s[3:4]="t"     ❌ 不在字典中
  j=2: s[2:4]="et"    ❌ 不在字典中
  j=1: s[1:4]="eet"   ❌ 不在字典中
  j=0: s[0:4]="leet"  ✅ 在字典中！
       → 递归调用 dfs(0)
       
dfs(0): 返回 True（基础情况）

回溯：dfs(0)→True, dfs(4)→True, dfs(8)→True
结果：True
```

## Subarray Sum = k
```code
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 滑动窗口依赖单调性, but nums[i] here can be positive / negative
        # Therefore, use prefix_sum
        # 1. build the prefix table
        prefix = [0] * (len(nums) + 1)
        for i, n in enumerate(nums):
            prefix[i + 1] = prefix[i] + n
        
        # 2. prefix[right] - prefix[left] = k, so prefix[left] = prefix[right] - k
        # We can loop through prefix as prefix[right] and sum the count = prefix[left]
        res = 0
        count = defaultdict(int)
        for p in prefix:
            res += count[p - k]
            count[p] += 1
        return res
```

## Max Subarray Sum
nums[i] non-negative -> sliding window w/ a dictionary to record the first-occur index

nums[i] can be negative -> prefix sum + dictionary to record all index
```code
from collections import defaultdict
from typing import List, Optional, Tuple

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> Optional[int]:
        """
        1. 用字典记录每个数字的所有出现位置和对应的前缀和
        3. 对每个有重复的数字，计算所有可能配对的子数组和
        4. 返回最大值
        """
        if not nums or len(nums) < 2:
            return None
        
        n = len(nums)
        max_sum = float('-inf')
        found_duplicate = False
        
        # 记录每个数字的所有出现位置和对应的前缀和
        # {num: [(index, prefix_sum_before_index), ...]}
        occurrences = defaultdict(list)
        prefix_sum = 0
        
        for j, num in enumerate(nums):
            if num in occurrences:
                found_duplicate = True
                
                # 计算与之前所有相同元素构成的子数组和
                for i, prev_prefix in occurrences[num]:
                    # sum(i to j) = current_prefix_sum + num - prev_prefix
                    subarray_sum = prefix_sum + num - prev_prefix
                    max_sum = max(max_sum, subarray_sum)
            
            # 记录当前位置和前缀和
            occurrences[num].append((j, prefix_sum))
            prefix_sum += num
        
        return max_sum if found_duplicate else None


def test_comprehensive():
    """全面测试函数"""
    solution = Solution()
    
    test_cases = [
        {
            'name': '基本正数情况',
            'nums': [1, 2, 3, 3, 4, 5, 5],
            'expected_explanation': '3到3: sum([3,3])=6 或 5到5: sum([5,5])=10'
        },
        {
            'name': '包含负数',
            'nums': [2, -3, 2, 1, 2],
            'expected_explanation': '第一个2到第二个2: sum([2,-3,2])=1 或 第一个2到第三个2: sum([2,-3,2,1,2])=4'
        },
        {
            'name': '负数导致中间更优',
            'nums': [5, -10, 3, -10, 5],
            'expected_explanation': '-10到-10: sum([-10,3,-10])=-17 或 5到5: sum([5,-10,3,-10,5])=-7'
        },
        {
            'name': '包含零',
            'nums': [0, 1, 2, 0, -1, 0],
            'expected_explanation': '需要考虑所有0的配对'
        },
        {
            'name': '多个相同元素',
            'nums': [1, 2, 1, 3, 1, -2, 1],
            'expected_explanation': '需要找出所有1配对中和最大的'
        },
        {
            'name': '全部相同',
            'nums': [3, 3, 3, 3],
            'expected_explanation': '最长的配对: 第一个到最后一个'
        },
        {
            'name': '负数数组',
            'nums': [-1, -2, -1, -3, -1],
            'expected_explanation': '找最小损失的配对'
        }
    ]
    
    for test in test_cases:
        print(f"\n测试: {test['name']}")
        print(f"输入: {test['nums']}")
        print(f"说明: {test['expected_explanation']}")
        
        # 使用两种方法验证
        result1 = solution.maxSubarraySum(test['nums'])
        
        print(f"最大和: {result1}")
        assert result1 == result2 == result_detail, "不同方法结果不一致！"
        
        if info:
            print(f"最优子数组: {info['subarray']}")
            print(f"位置: [{info['start_index']}, {info['end_index']}]")
            print(f"重复值: {info['value']}")
    
    # 性能测试
    print("\n\n=== 性能测试 ===")
    import time
    import random
    
    # 生成大数组
    large_nums = [random.randint(-100, 100) for _ in range(1000)]
    # 确保有重复
    large_nums.extend([50] * 10)
    random.shuffle(large_nums)
    
    start = time.time()
    result = solution.maxSubarraySum(large_nums)
    end = time.time()
    
    print(f"数组大小: {len(large_nums)}")
    print(f"执行时间: {(end - start) * 1000:.2f}ms")
    print(f"结果: {result}")
    
    # 边界情况测试
    print("\n=== 边界情况 ===")
    edge_cases = [
        ([], "空数组"),
        ([1], "单个元素"),
        ([1, 2], "无重复"),
        ([1, 1], "两个相同元素"),
        ([0, 0, 0], "全零")
    ]
    
    for nums, description in edge_cases:
        result = solution.maxSubarraySum(nums)
        print(f"{description}: {nums} -> {result}")


if __name__ == "__main__":
    test_comprehensive()
```

## 换一个元素->最长非递减子数组的长度
```code
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 1

        suf = [0] * n
        suf[-1] = 1
        ans = 2
        for i in range(n - 2, 0, -1):
            if nums[i] <= nums[i + 1]:
                suf[i] = suf[i + 1] + 1
                ans = max(ans, suf[i] + 1)  # 把 nums[i-1] 拼在 suf[i] 前面
            else:
                suf[i] = 1

        pre = 1
        for i in range(1, n - 1):
            if nums[i - 1] <= nums[i + 1]:
                ans = max(ans, pre + 1 + suf[i + 1])  # 替换 nums[i]
            if nums[i - 1] <= nums[i]:
                pre += 1
                ans = max(ans, pre + 1)  # 把 nums[i+1] 拼在 pre 后面
            else:
                pre = 1
        return ans
```

## Median
在两个有序数组中，查找第 k 小的数，其中 k=(m+n)/2

如果 m+n 是奇数，返回第 k 小的数。
如果 m+n 是偶数，返回第 k 小的数和第 k+1 小的数的平均值。
```code
class Solution:
    def findMedianSortedArrays(self, a: List[int], b: List[int]) -> float:
        if len(a) > len(b):
            a, b = b, a

        m, n = len(a), len(b)
        a = [-inf] + a + [inf]
        b = [-inf] + b + [inf]

        # 循环不变量：a[left] <= b[j+1]
        # 循环不变量：a[right] > b[j+1]
        left, right = 0, m + 1
        while left + 1 < right:  # 开区间 (left, right) 不为空
            i = (left + right) // 2
            j = (m + n + 1) // 2 - i
            if a[i] <= b[j + 1]:
                left = i  # 缩小二分区间为 (i, right)
            else:
                right = i  # 缩小二分区间为 (left, i)

        # 此时 left 等于 right-1
        # a[left] <= b[j+1] 且 a[right] > b[j'+1] = b[j]，所以答案是 i=left
        i = left
        j = (m + n + 1) // 2 - i
        max1 = max(a[i], b[j])
        min2 = min(a[i + 1], b[j + 1])
        return max1 if (m + n) % 2 else (max1 + min2) / 2
```

## MedianFinder
```code
class MedianFinder:
    def __init__(self):
        self.left = []  # 入堆的元素取相反数，变成最大堆
        self.right = []  # 最小堆

    def addNum(self, num: int) -> None:
        if len(self.left) == len(self.right):
            heappush(self.left, -heappushpop(self.right, num))
        else:
            heappush(self.right, -heappushpop(self.left, -num))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return -self.left[0]
        return (self.right[0] - self.left[0]) / 2
```

## 最小旅行成本
```code
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Optional
import heapq
import sys

class CityTravelOptimizer:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.cities = set()
    
    def addConnection(self, city1: str, city2: str, cost: int):
        """添加城市间的连接和成本"""
        self.graph[city1][city2] = cost
        self.graph[city2][city1] = cost
        self.cities.add(city1)
        self.cities.add(city2)
    
    def findLeastCostStartCity(self, connections: List[List]) -> Tuple[str, int]:
        """
        找到作为起点成本最小的城市
        
        Args:
            connections: [[city1, city2, cost], ...]
            
        Returns:
            (最佳起始城市, 最小成本)
        """
        # 构建图
        for city1, city2, cost in connections:
            self.addConnection(city1, city2, cost)
        
        min_cost = float('inf')
        best_start_city = None
        
        # 尝试从每个城市出发
        for start_city in self.cities:
            # 计算从该城市出发遍历所有城市的成本
            cost = self.calculateTravelCost(start_city)
            
            if cost < min_cost:
                min_cost = cost
                best_start_city = start_city
        
        return best_start_city, min_cost
    
    def calculateTravelCost(self, start_city: str) -> int:
        """
        计算从指定城市出发遍历所有城市并返回的最小成本
        使用动态规划解决TSP问题
        """
        cities_list = list(self.cities)
        n = len(cities_list)
        city_index = {city: i for i, city in enumerate(cities_list)}
        
        # 如果城市数量较少，使用精确的DP解法
        if n <= 15:
            return self.tsp_dp(start_city, city_index, cities_list)
        else:
            # 城市数量较多时使用近似算法
            return self.tsp_greedy(start_city)
    
    def tsp_dp(self, start_city: str, city_index: dict, cities_list: list) -> int:
        """
        使用动态规划精确求解TSP
        状态：dp[mask][i] = 从起点出发，访问了mask中的城市，当前在城市i的最小成本
        """
        n = len(cities_list)
        start_idx = city_index[start_city]
        
        # dp[mask][i] = 访问了mask表示的城市集合，当前在城市i的最小成本
        dp = [[float('inf')] * n for _ in range(1 << n)]
        
        # 初始状态：只访问起始城市
        dp[1 << start_idx][start_idx] = 0
        
        # 遍历所有可能的状态
        for mask in range(1 << n):
            for u in range(n):
                if dp[mask][u] == float('inf'):
                    continue
                
                # 尝试访问下一个未访问的城市
                for v in range(n):
                    if mask & (1 << v):  # 已访问
                        continue
                    
                    city_u = cities_list[u]
                    city_v = cities_list[v]
                    
                    if city_v in self.graph[city_u]:
                        new_mask = mask | (1 << v)
                        new_cost = dp[mask][u] + self.graph[city_u][city_v]
                        dp[new_mask][v] = min(dp[new_mask][v], new_cost)
        
        # 计算返回起点的成本
        full_mask = (1 << n) - 1
        min_cost = float('inf')
        
        for i in range(n):
            if i == start_idx:
                continue
            city_i = cities_list[i]
            if start_city in self.graph[city_i]:
                total_cost = dp[full_mask][i] + self.graph[city_i][start_city]
                min_cost = min(min_cost, total_cost)
        
        return min_cost
    
    def tsp_greedy(self, start_city: str) -> int:
        """
        使用贪心算法（最近邻居）近似求解TSP
        适用于城市数量较多的情况
        """
        visited = {start_city}
        current = start_city
        total_cost = 0
        
        while len(visited) < len(self.cities):
            # 找到最近的未访问城市
            min_dist = float('inf')
            next_city = None
            
            for neighbor, cost in self.graph[current].items():
                if neighbor not in visited and cost < min_dist:
                    min_dist = cost
                    next_city = neighbor
            
            if next_city:
                total_cost += min_dist
                visited.add(next_city)
                current = next_city
            else:
                break
        
        # 返回起点
        if start_city in self.graph[current]:
            total_cost += self.graph[current][start_city]
        
        return total_cost
    
    def convertToTree(self, root: str) -> Dict:
        """
        将图转换为树结构（使用BFS生成树）
        
        Returns:
            树的邻接表表示
        """
        tree = defaultdict(list)
        visited = {root}
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    tree[node].append(neighbor)
                    queue.append(neighbor)
        
        return dict(tree)
    
    def convertToMinSpanningTree(self) -> Dict:
        """
        将图转换为最小生成树（使用Kruskal算法）
        """
        # 收集所有边
        edges = []
        seen = set()
        
        for city1 in self.graph:
            for city2, cost in self.graph[city1].items():
                edge = tuple(sorted([city1, city2]))
                if edge not in seen:
                    edges.append((cost, city1, city2))
                    seen.add(edge)
        
        # 按成本排序
        edges.sort()
        
        # 并查集
        parent = {city: city for city in self.cities}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        
        # 构建最小生成树
        tree = defaultdict(list)
        total_cost = 0
        
        for cost, city1, city2 in edges:
            if union(city1, city2):
                tree[city1].append((city2, cost))
                tree[city2].append((city1, cost))
                total_cost += cost
        
        return dict(tree), total_cost


# 简化版解决方案（针对面试）
class SimpleCityTravel:
    def findBestStartCity(self, connections: List[List]) -> Tuple[str, int]:
        """
        简化版：找到最优起始城市
        
        Args:
            connections: [["A", "B", 10], ["B", "C", 20], ...]
        
        Returns:
            (最佳起始城市, 最小成本)
        """
        # 构建图
        graph = defaultdict(dict)
        cities = set()
        
        for city1, city2, cost in connections:
            graph[city1][city2] = cost
            graph[city2][city1] = cost
            cities.add(city1)
            cities.add(city2)
        
        def dijkstra(start):
            """从start出发到所有其他城市的最短路径"""
            distances = {city: float('inf') for city in cities}
            distances[start] = 0
            visited = set()
            heap = [(0, start)]
            
            while heap:
                curr_dist, curr_city = heapq.heappop(heap)
                
                if curr_city in visited:
                    continue
                
                visited.add(curr_city)
                
                for neighbor, cost in graph[curr_city].items():
                    new_dist = curr_dist + cost
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(heap, (new_dist, neighbor))
            
            return distances
        
        # 计算每个城市作为起点的总成本
        min_total_cost = float('inf')
        best_city = None
        
        for start_city in cities:
            # 获取从该城市到所有其他城市的最短距离
            distances = dijkstra(start_city)
            
            # 计算访问所有城市的总成本（简化：使用最短路径之和）
            total_cost = sum(distances.values())
            
            if total_cost < min_total_cost:
                min_total_cost = total_cost
                best_city = start_city
        
        return best_city, min_total_cost


def test_solution():
    """测试函数"""
    print("=== 城市旅行成本优化测试 ===\n")
    
    # 测试用例1：简单三角形
    print("测试1：三城市三角形")
    optimizer = CityTravelOptimizer()
    connections1 = [
        ["A", "B", 10],
        ["B", "C", 20],
        ["A", "C", 15]
    ]
    
    best_city, min_cost = optimizer.findLeastCostStartCity(connections1)
    print(f"连接: {connections1}")
    print(f"最佳起始城市: {best_city}")
    print(f"最小成本: {min_cost}")
    
    # 转换为树
    tree = optimizer.convertToTree(best_city)
    print(f"树结构: {tree}\n")
    
    # 测试用例2：四城市网络
    print("测试2：四城市完全图")
    optimizer2 = CityTravelOptimizer()
    connections2 = [
        ["北京", "上海", 100],
        ["北京", "广州", 150],
        ["北京", "深圳", 200],
        ["上海", "广州", 120],
        ["上海", "深圳", 130],
        ["广州", "深圳", 50]
    ]
    
    best_city2, min_cost2 = optimizer2.findLeastCostStartCity(connections2)
    print(f"最佳起始城市: {best_city2}")
    print(f"最小旅行成本: {min_cost2}")
    
    # 最小生成树
    mst, mst_cost = optimizer2.convertToMinSpanningTree()
    print(f"最小生成树总成本: {mst_cost}")
    print(f"树结构: {dict(mst)}\n")
    
    # 测试简化版
    print("测试3：简化版算法")
    simple = SimpleCityTravel()
    best_city3, cost3 = simple.findBestStartCity(connections2)
    print(f"最佳起始城市（简化）: {best_city3}")
    print(f"成本估算: {cost3}")


if __name__ == "__main__":
    test_solution()
```

## Highway Checkpoint
```code
from collections import defaultdict
import re
from typing import List

class TollCalculator:
    def calculateTolls(self, logs: List[str]) -> List[str]:
        """
        计算每辆车的总过路费
        
        Args:
            logs: 日志列表，格式为 "车牌,收费站,时间戳"
            
        Returns:
            格式化的费用列表 ["License: 车牌, Fee: 费用"]
        """
        # Step 1: 解析日志并按车牌分组
        vehicle_logs = defaultdict(list)
        
        for log in logs:
            # 解析日志条目
            parts = log.split(',')
            license_plate = parts[0]
            checkpoint = parts[1]
            timestamp = int(parts[2])
            
            # 提取收费站位置（数字部分）
            position = self.extractPosition(checkpoint)
            
            # 记录：(时间戳, 位置, 收费站名称)
            vehicle_logs[license_plate].append((timestamp, position, checkpoint))
        
        # Step 2: 计算每辆车的费用
        results = []
        
        for license_plate, checkpoint_records in vehicle_logs.items():
            # 按时间戳排序
            checkpoint_records.sort(key=lambda x: x[0])
            
            # 计算总费用
            total_fee = 0
            for i in range(1, len(checkpoint_records)):
                prev_position = checkpoint_records[i-1][1]
                curr_position = checkpoint_records[i][1]
                
                # 费用 = |位置差| × 10
                fee = abs(curr_position - prev_position) * 10
                total_fee += fee
            
            # 格式化结果
            results.append(f"License: {license_plate}, Fee: {total_fee}")
        
        return results
    
    def extractPosition(self, checkpoint: str) -> int:
        """
        从收费站名称中提取位置数字
        
        Args:
            checkpoint: 收费站名称（如 "A5", "D10"）
            
        Returns:
            位置数字
        """
        # 使用正则表达式提取数字
        match = re.search(r'\d+', checkpoint)
        if match:
            return int(match.group())
        return 0
    
    def calculateTollsWithDetails(self, logs: List[str]) -> dict:
        """
        计算费用并返回详细信息
        
        Returns:
            包含详细路线和费用信息的字典
        """
        vehicle_logs = defaultdict(list)
        
        # 解析日志
        for log in logs:
            parts = log.split(',')
            license_plate = parts[0]
            checkpoint = parts[1]
            timestamp = int(parts[2])
            position = self.extractPosition(checkpoint)
            
            vehicle_logs[license_plate].append({
                'timestamp': timestamp,
                'position': position,
                'checkpoint': checkpoint
            })
        
        # 计算详细费用
        detailed_results = {}
        
        for license_plate, records in vehicle_logs.items():
            # 按时间排序
            records.sort(key=lambda x: x['timestamp'])
            
            route = []
            segments = []
            total_fee = 0
            
            for i in range(len(records)):
                route.append(f"{records[i]['checkpoint']}({records[i]['position']})")
                
                if i > 0:
                    prev = records[i-1]
                    curr = records[i]
                    
                    distance = abs(curr['position'] - prev['position'])
                    fee = distance * 10
                    
                    segments.append({
                        'from': prev['checkpoint'],
                        'to': curr['checkpoint'],
                        'distance': distance,
                        'fee': fee
                    })
                    
                    total_fee += fee
            
            detailed_results[license_plate] = {
                'route': ' → '.join(route),
                'segments': segments,
                'total_fee': total_fee
            }
        
        return detailed_results


def test_toll_calculator():
    """测试函数"""
    calculator = TollCalculator()
    
    # 测试用例1
    print("=== 测试用例1 ===")
    logs1 = ["CAR123,A1,1000", "CAR123,A5,2000"]
    result1 = calculator.calculateTolls(logs1)
    print(f"输入: {logs1}")
    print(f"输出: {result1}")
    print(f"解释: A1(位置1) → A5(位置5), 费用 = |5-1|×10 = 40")
    
    # 测试用例2
    print("\n=== 测试用例2 ===")
    logs2 = [
        "CAR111,C2,1100", 
        "CAR111,C4,1300", 
        "CAR222,C1,1000", 
        "CAR222,C3,1500", 
        "CAR222,C7,2000"
    ]
    result2 = calculator.calculateTolls(logs2)
    details2 = calculator.calculateTollsWithDetails(logs2)
    
    print(f"输入: {logs2}")
    print(f"输出: {result2}")
    print("\n详细信息:")
    for license, info in details2.items():
        print(f"\n{license}:")
        print(f"  路线: {info['route']}")
        for segment in info['segments']:
            print(f"  - {segment['from']} → {segment['to']}: "
                  f"距离={segment['distance']}, 费用={segment['fee']}")
        print(f"  总费用: {info['total_fee']}")
    
    # 测试用例3：时间戳不按顺序
    print("\n=== 测试用例3 ===")
    logs3 = [
        "CAR999,D10,3000", 
        "CAR999,D1,1000", 
        "CAR999,D5,2000"
    ]
    result3 = calculator.calculateTolls(logs3)
    details3 = calculator.calculateTollsWithDetails(logs3)
    
    print(f"输入: {logs3}")
    print(f"输出: {result3}")
    print(f"\n按时间排序后的路线: {details3['CAR999']['route']}")
    print(f"费用计算:")
    for segment in details3['CAR999']['segments']:
        print(f"  {segment['from']} → {segment['to']}: {segment['fee']}")
    print(f"总费用: {details3['CAR999']['total_fee']}")
    
    # 测试用例4：复杂场景
    print("\n=== 测试用例4：复杂场景 ===")
    logs4 = [
        "CAR001,A1,1000",
        "CAR001,A10,2000",
        "CAR001,A5,3000",
        "CAR001,A8,4000",
        "CAR002,B20,1500",
        "CAR002,B5,2500",
        "CAR002,B15,3500"
    ]
    result4 = calculator.calculateTolls(logs4)
    details4 = calculator.calculateTollsWithDetails(logs4)
    
    print(f"输入: {logs4}")
    print(f"输出: {result4}")
    print("\n详细路线:")
    for license, info in details4.items():
        print(f"\n{license}: {info['route']}")
        print(f"  总费用: {info['total_fee']}")
    
    # 边界情况测试
    print("\n=== 边界情况测试 ===")
    
    # 同一位置
    logs5 = ["CAR555,X5,1000", "CAR555,Y5,2000"]
    result5 = calculator.calculateTolls(logs5)
    print(f"同一位置测试: {logs5}")
    print(f"结果: {result5} (费用应为0)")
    
    # 大位置数字
    logs6 = ["CAR666,Z100,1000", "CAR666,Z1,2000"]
    result6 = calculator.calculateTolls(logs6)
    print(f"\n大数字测试: {logs6}")
    print(f"结果: {result6} (费用 = |100-1|×10 = 990)")


# 优化版本：支持批量处理
class OptimizedTollCalculator:
    def calculateTolls(self, logs: List[str]) -> List[str]:
        """优化版本，减少内存使用"""
        # 使用单次遍历完成解析和分组
        vehicle_data = {}
        
        for log in logs:
            license, checkpoint, timestamp = log.split(',')
            position = int(''.join(filter(str.isdigit, checkpoint)))
            
            if license not in vehicle_data:
                vehicle_data[license] = []
            
            vehicle_data[license].append((int(timestamp), position))
        
        results = []
        
        for license, checkpoints in vehicle_data.items():
            # 原地排序
            checkpoints.sort()
            
            # 计算费用
            total_fee = sum(
                abs(checkpoints[i][1] - checkpoints[i-1][1]) * 10
                for i in range(1, len(checkpoints))
            )
            
            results.append(f"License: {license}, Fee: {total_fee}")
        
        return results


if __name__ == "__main__":
    test_toll_calculator()
```
