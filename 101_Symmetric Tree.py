# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def check(self, n1: Optional[TreeNode], n2: Optional[TreeNode]) -> bool:
        # case: both None, one None, both not None but different value, both not None and same value -> check children
        if n1 == None and n2 == None: return True
        if (not n1) or (not n2) or (n1.val != n2.val): return False
        return self.check(n1.right, n2.left) and self.check(n1.left, n2.right)
    
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        return self.check(root.left, root.right)
        