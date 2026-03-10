# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def bs(l: int, r: int) -> Optional[TreeNode]:
            if l > r: return None
            m = (l + r) >> 1
            return TreeNode(nums[m], bs(l, m-1), bs(m+1, r))
        return bs(0, len(nums)-1)