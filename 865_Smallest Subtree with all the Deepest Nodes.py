# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Key Insight: subtree.left = subtree.right = maxDepth -> post-order
        maxDepth, subtree = 0, None

        def post(node, depth) -> int:
            nonlocal maxDepth, subtree

            # 1. update maxDepth when over the leafnode
            if not node:
                maxDepth = max(maxDepth, depth)
                return depth
            # 2. target subtree has the l/r branch both with the maxDepth
            left = post(node.left, depth + 1)
            right = post(node.right, depth + 1)
            
            if left == right == maxDepth: subtree = node
            return max(left, right)
        
        post(root, 0)
        return subtree