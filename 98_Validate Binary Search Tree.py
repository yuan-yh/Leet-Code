# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node: Optional[TreeNode], minVal: int, maxVal: int) -> bool:
            if not node: return True

            return (minVal < node.val < maxVal) and validate(node.left, minVal, min(node.val, maxVal)) and validate(node.right, max(node.val, minVal), maxVal)

        return validate(root, -inf, inf)