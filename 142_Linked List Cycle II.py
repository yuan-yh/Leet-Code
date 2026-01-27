# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Let a = head to cycle start, b = head to meet, c = cycle length.
        fast = b + kc = 2 * slow = 2 * b, so b = kc.

        For the slow ptr moves b-a step in the cycle, it will complete cycles and reach the cycle start by moving a steps.
        """
        fast = slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            if fast == slow:
                while head != slow:
                    head = head.next
                    slow = slow.next
                return head
        return None