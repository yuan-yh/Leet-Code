# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        mod = 10**9 + 7
        subtree = []
        # 1. record subtree sum - post-order
        def post(node) -> int:
            if not node: return 0
            cur = post(node.left) + post(node.right) + node.val
            subtree.append(cur)
            return cur

        total = post(root)

        # 2. for each subtree, calculate tree product
        res = max(s * (total-s) for s in subtree)
        return res%mod