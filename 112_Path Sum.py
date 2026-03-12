# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], target: int) -> bool:
        # DFS: terminate when leafnode or curSum > target
        if root == None: return False
        target -= root.val
        if (root.left == None and root.right == None): return target == 0
        return self.hasPathSum(root.left, target) or self.hasPathSum(root.right, target)