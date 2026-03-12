# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        def bt(node: Optional[TreeNode], target):
            if node == None: return

            curPath.append(node.val)
            target -= node.val

            if node.left == None and node.right == None:
                if target == 0: res.append(list(curPath))
                curPath.pop()
                return
            
            bt(node.left, target)
            bt(node.right, target)
            curPath.pop()

        res, curPath = [], []
        bt(root, targetSum)
        return res