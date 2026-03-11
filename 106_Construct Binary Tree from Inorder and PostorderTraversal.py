# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        # inorder: l - m - r; post: l - r - m
        # 1. hash idx of inorder
        idx = {n : i for i, n in enumerate(inorder)}
        
        def dfs(il, pl, pr) -> Optional[TreeNode]:
            if pl >= pr: return None 

            root = TreeNode(postorder[pr-1])
            i = idx[root.val]
            left_size = i - il

            root.left = dfs(il, pl, pl+left_size)
            root.right = dfs(i+1, pl+left_size, pr-1)
            return root
        
        return dfs(0, 0, len(postorder))
