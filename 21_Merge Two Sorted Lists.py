# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # merge l2 into l1
        # 1. short-cut
        if not l2: return l1

        # 2. loop: insert l2 into l1 (cur.next.val vs l2.val)
        vHead = cur = ListNode(0, l1)
        while l2:
            # case: l1 empty; case: l1.val vs l2.val
            if cur.next == None:
                cur.next = l2
                break
            if cur.next.val <= l2.val:
                cur = cur.next
            else:
                t1, t2 = cur.next, l2.next
                cur.next = l2
                l2.next = t1
                cur = l2
                l2 = t2

        return vHead.next