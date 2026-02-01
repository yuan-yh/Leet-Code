# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        vHead = cur = ListNode(0, head)

        # 1. loop before the left idx
        for _ in range(left-1):
            if cur: cur = cur.next
        if not cur: return head

        # 2. reverse
        otail, rtail = cur, cur.next
        cur = cur.next
        rHead = ListNode()

        for _ in range(right - left + 1):
            if not cur: break

            tmp = cur.next
            cur.next = rHead.next
            rHead.next = cur
            cur = tmp
        
        # 3. connect
        otail.next = rHead.next
        rtail.next = cur
        
        return vHead.next