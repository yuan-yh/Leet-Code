# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# Method 1: Recursion
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        return 0 if not root else 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

# Method 2: Iteration (BFS)
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        q = deque()
        if root:
            q.append(root)
        
        # BFS
        depth = 0
        while q:
            cnt = len(q)
            depth += 1
            for _ in range(cnt):
                tmp = q.popleft()
                if tmp.left: 
                    q.append(tmp.left)
                if tmp.right:
                    q.append(tmp.right)

        return depth