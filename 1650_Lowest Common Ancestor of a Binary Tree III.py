"""
# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
"""

class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        """
        Let a = p -> lca, b = q -> lca, c = lca -> head.
        ptrP = a + c + b, ptrQ = b + c + a (switch to another node)
        Same as LC160
        """
        ptrP, ptrQ = p, q

        while ptrP != ptrQ:
            ptrP = ptrP.parent if ptrP else q
            ptrQ = ptrQ.parent if ptrQ else p
        
        return ptrP