# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        """
        Let both pointers walk the same distance to meet at the intersection.
        p1 = headA_to_intersection + same + headB_to_intersection
        p2 = headB_to_intersection + same + headA_to_intersection
        For no-intersection case, consider 'tail -> None' as the intersection.
        """
        pA, pB = headA, headB

        while pA != pB:
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA
        return pA