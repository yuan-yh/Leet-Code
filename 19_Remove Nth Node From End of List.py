# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Key Insight: fast/slow ptr w/ n gaps
        fast = slow = vHead = ListNode(0, head)
        
        # 1. shift the fast ptr n nodes
        for _ in range(n): fast = fast.next

        # 2. shift the slow/fast ptr together until fast.next reached the end
        while fast.next:
            fast = fast.next
            slow = slow.next
        
        slow.next = slow.next.next

        return vHead.next