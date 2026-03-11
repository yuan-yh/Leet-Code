# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    # Method 1: reverse-pre: right-left-mid (头插法)
    head = None

    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root: return

        self.flatten(root.right)
        self.flatten(root.left)

        root.left = None
        root.right = self.head
        self.head = root


    # # Method 2: simulate pre-order
    # def flatten(self, root: Optional[TreeNode]) -> None:
    #     """
    #     Do not return anything, modify root in-place instead.
    #     """
    #     # Pre-Order
    #     vHead = cur = TreeNode()

    #     def pre(node: Optional[TreeNode]):
    #         if not node: return

    #         nonlocal cur
    #         cur.right = node
    #         cur = cur.right
    #         tmpl, tmpr = cur.left, cur.right
    #         cur.left = cur.right = None

    #         pre(tmpl)
    #         pre(tmpr)
        
    #     pre(root)