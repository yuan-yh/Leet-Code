# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        res = -inf

        # path case: left-root-right OR max(left, right)-root-next -> post-order
        def post(node: Optional[TreeNode]) -> int:
            if not node: return 0

            l, r = post(node.left), post(node.right)
            nonlocal res
            res = max(res, l+node.val+r)
            return max(max(l, r) + node.val, 0)     # discard negative branch
        
        post(root)
        return res