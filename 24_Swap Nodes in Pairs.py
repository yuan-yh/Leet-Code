# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vHead = cur = ListNode(0, head)
        
        while cur.next and cur.next.next:
            t1 = cur.next
            t2 = cur.next.next if t1 else None

            # reconnect
            t1.next = t2.next
            t2.next = t1
            cur.next = t2

            # update
            cur = t1

        return vHead.next