# 分析与解题思路

**题意理解：**
给定一个数组，指定每个节点的父节点，判断是否是一棵合法的树。

**关键条件：**
1. 树需要满足存在 n-1 条边
2. 从根节点到任意节点都仅有一条简单路径
3. 树必须恰好有一个根节点（父节点为-1的节点）

**解题思路：**
1. 首先检查根节点数量是否为1（父节点为-1的节点）
2. 构建邻接表表示父子关系
3. 从根节点开始进行遍历（DFS或BFS），标记访问过的节点
4. 在遍历过程中，通过标记数组判断每个节点是否只访问了一次
5. 遍历完成后，检查是否所有节点都被访问过

**实现细节：**
- 如果发现某个节点被访问多次，说明存在环或多条路径，返回 false
- 如果遍历结束后还有节点未被访问，说明树不连通，返回 false

# Python 代码实现

```python
def is_valid_tree(parents):
    """
    判断给定的父节点数组是否构成一棵合法的树
    
    参数:
        parents: 列表，parents[i] 表示节点 i 的父节点，根节点的父节点为 -1
    
    返回:
        bool: 如果是合法的树返回 True，否则返回 False
    """
    n = len(parents)
    
    # 特殊情况：空树或单节点
    if n == 0:
        return True
    if n == 1:
        return parents[0] == -1
    
    # 1. 检查根节点数量（父节点为-1的节点）
    root_count = 0
    root = -1
    for i in range(n):
        if parents[i] == -1:
            root_count += 1
            root = i
    
    # 必须恰好有一个根节点
    if root_count != 1:
        return False
    
    # 2. 构建邻接表（父节点到子节点的映射）
    children = [[] for _ in range(n)]
    for i in range(n):
        if parents[i] != -1:
            children[parents[i]].append(i)
    
    # 3. 从根节点开始DFS遍历，标记访问过的节点
    visited = [False] * n
    
    def dfs(node):
        # 如果节点已被访问，说明有环或多条路径
        if visited[node]:
            return False
        
        visited[node] = True
        
        # 遍历所有子节点
        for child in children[node]:
            if not dfs(child):
                return False
        
        return True
    
    # 从根节点开始遍历
    if not dfs(root):
        return False
    
    # 4. 检查是否所有节点都被访问过
    for i in range(n):
        if not visited[i]:
            return False
    
    return True


# 测试用例
if __name__ == "__main__":
    # 测试用例1：合法的树
    # 结构：  0
    #        / \
    #       1   2
    #          /
    #         3
    test1 = [-1, 0, 0, 2]
    print(f"测试1: {test1} -> {is_valid_tree(test1)}")  # True
    
    # 测试用例2：有环的图
    test2 = [1, 0, 0]
    print(f"测试2: {test2} -> {is_valid_tree(test2)}")  # False
    
    # 测试用例3：多个根节点
    test3 = [-1, 0, -1]
    print(f"测试3: {test3} -> {is_valid_tree(test3)}")  # False
    
    # 测试用例4：不连通的森林
    test4 = [-1, 0, 3, -1]
    print(f"测试4: {test4} -> {is_valid_tree(test4)}")  # False
    
    # 测试用例5：单节点
    test5 = [-1]
    print(f"测试5: {test5} -> {is_valid_tree(test5)}")  # True
```

**时间复杂度：** O(n)，其中 n 是节点数量，每个节点访问一次  
**空间复杂度：** O(n)，用于存储邻接表和访问标记数组