# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        # In-Order
        k -= 1  # make it 0-index

        def inorder(node: Optional[TreeNode]):
            # 1. end case
            if not node: return -1

            # 2. process left
            left = inorder(node.left)
            if left != -1: return left

            # 3. process cur-node
            nonlocal k
            if k == 0: return node.val
            k -= 1

            # 4. process right
            return inorder(node.right)
        
        return inorder(root)