# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # 1. hash in-order
        index = {n : i for i, n in enumerate(inorder)}

        # 2. if idx c such that inorder[c] = preorder[0], the left_size = c - 0
        def dfs(pl, pr, il) -> Optional[TreeNode]:
            if pl >= pr: return None

            root = TreeNode(preorder[pl])

            i = index[preorder[pl]]
            left_size = i - il
            root.left = dfs(pl+1, pl+1+left_size, il)
            root.right = dfs(pl+1+left_size, pr, i+1)

            return root

        return dfs(0, len(preorder), 0)