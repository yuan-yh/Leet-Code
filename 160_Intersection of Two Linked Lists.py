# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        """
        Let a = A to intersection, b = B to intersection, c = intersection to end.
        Have 2 ptrs starting from headA and headB, switch to dif head when reach end, then they will meet in the intersection.
        Because ptrA: a + c + b == ptrB: b + c + a
        """
        pA, pB = headA, headB

        while pA != pB:
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA
        return pA