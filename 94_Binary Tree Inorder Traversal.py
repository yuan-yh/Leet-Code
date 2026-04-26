# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    # Iteration
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        stack = []
        cur = root

        while stack or cur:
            # 1. dive into the leftmost branch of cur_node until bottom
            while cur:
                stack.append(cur)
                cur = cur.left
            # 2. process, update, then ready to dive the right node
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        return res
    
    # # Recursion
    # def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    #     # end case
    #     if not root: return []
    #     # process
    #     left = self.inorderTraversal(root.left)
    #     return left + [root.val] + self.inorderTraversal(root.right)