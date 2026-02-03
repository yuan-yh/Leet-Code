# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        foundP = foundQ = False

        def helper(node: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
            nonlocal foundP, foundQ
            if not node: return None
            if node == p: foundP = True
            if node == q: foundQ = True

            left = helper(node.left, p, q)
            right = helper(node.right, p, q)

            if (left and right) or (node == p) or (node == q): return node
            return left if left else right
        
        lca = helper(root, p, q)
        return lca if (foundP and foundQ) else None