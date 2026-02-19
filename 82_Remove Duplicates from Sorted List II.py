# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Remove all nodes w/ duplicates -> 2-ptr
        vHead = cur = ListNode(0, head)

        # We only worry about the next duplicates when >= 2 next nodes
        while cur.next and cur.next.next:
            value = cur.next.val
            # case: next duplicate -> skip all next-dups
            if cur.next.next.val == value:
                while cur.next and cur.next.val == value:
                    cur.next = cur.next.next
            # case: next not duplicate -> attach & proceed
            else:
                cur = cur.next
        return vHead.next
