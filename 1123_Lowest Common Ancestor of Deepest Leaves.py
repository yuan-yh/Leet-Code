# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Key Insight: LCA of deepest leaves = lowest deepest-subtree (LC865)
        lca, maxDepth = None, 0

        def post(node, depth) -> int:
            nonlocal lca, maxDepth
            # 1. update maxDepth when over the leafnode
            if not node:
                maxDepth = max(maxDepth, depth)
                return depth
            # 2. For lca of the deepest node, its left_len = right_len = maxDepth
            left = post(node.left, depth + 1)
            right = post(node.right, depth + 1)

            if left == right == maxDepth: lca = node
            return max(left, right)
            
        post(root, 0)
        return lca