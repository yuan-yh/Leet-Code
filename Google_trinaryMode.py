# 三叉树：
# 左子节点值 < 父节点值
# 中子节点值 = 父节点值
# 右子节点值 > 父节点值

这棵树的结构其实和 BST 很像，中子节点存的是重复值。所以某个值出现的次数，就等于从它第一次出现的节点开始，沿着 middle child 链往下走的长度 + 1。
最优解法：中序遍历（In-order Traversal）
因为树的性质类似 BST，中序遍历会得到一个有序序列，相同的值会连续出现。我们可以一边遍历一边统计。
时间复杂度 O(n)，空间复杂度 O(h)（h 为树高，递归栈）。

class Node:
    def __init__(self, val, left=None, mid=None, right=None):
        self.val = val
        self.left = left
        self.mid = mid
        self.right = right

def find_mode(root):
    best_count = 0
    best_val = None
    cur_count = 0
    cur_val = None

    def inorder(node):
        nonlocal best_count, best_val, cur_count, cur_val
        if not node:
            return
        # 左 -> 当前 -> 中 -> 右（中序）
        inorder(node.left)

        # 处理当前节点
        if node.val == cur_val:
            cur_count += 1
        else:
            cur_val = node.val
            cur_count = 1

        if cur_count > best_count:
            best_count = cur_count
            best_val = cur_val

        inorder(node.mid)  # 中子节点值相同，继续累加
        inorder(node.right)

    inorder(root)
    return best_val

Follow-up：Broken Tree
"Broken tree" 通常指的是树的结构被破坏了，即某些节点不满足三叉树的性质（比如左子节点的值不再小于父节点）。
可能的问法

检测 broken 的节点：类似 "Validate BST"，中序遍历时检查是否有序。
在 broken tree 上求 mode：既然不能依赖有序性质，就需要用 HashMap 来统计每个值的频率。
def find_mode_broken(root):
    from collections import defaultdict
    count = defaultdict(int)

    def dfs(node):
        if not node:
            return
        count[node.val] += 1
        dfs(node.left)
        dfs(node.mid)
        dfs(node.right)

    dfs(root)
    return max(count, key=count.get)

这种情况下时间复杂度还是 O(n)，但空间复杂度变成 O(n)（HashMap 存所有不同的值），比正常树的 O(h) 要差。
面试中的回答思路
面试官问 broken tree，核心考点是：你之前的解法依赖了树的有序性质，如果这个性质不成立了，你怎么调整？答案就是退化到通用的 HashMap 计数方法。