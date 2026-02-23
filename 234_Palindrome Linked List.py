# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def findMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # odd: middle; even: right-half start
        fast = slow = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, cur = None, head
        while cur:
            tmp = cur.next
            cur.next = prev
            prev = cur
            cur = tmp
        return prev

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        For even case: 1-2-2-1, after reverse is 1->2->2 and 1->2 (both point to mid but one extra on left)
        For odd case: 1-2-1, after reverse is 1->2 and 1->2 (both point to mid)
        """
        # 1. find middle
        mid = self.findMiddle(head)
        # 2. reverse
        p2 = self.reverse(mid)
        # 3. compare
        p1 = head
        while p2:
            if p1.val != p2.val: return False
            p1 = p1.next
            p2 = p2.next
        return True