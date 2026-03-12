# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], target: int) -> int:
        """
        curSum = sum(node) along the visited branch
        if curSum - target exists in prefix, there must exist a sub-branch sum to target
        """
        def bt(node: Optional[TreeNode], curSum: int):
            if not node: return

            curSum += node.val
            nonlocal cnt
            cnt += prefix[curSum - target]

            prefix[curSum] += 1
            bt(node.left, curSum)
            bt(node.right, curSum)
            prefix[curSum] -= 1
        
        prefix = defaultdict(int)
        prefix[0] = 1
        cnt = 0
        bt(root, 0)
        return cnt