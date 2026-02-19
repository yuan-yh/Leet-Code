// Time complexity: O(n)
// Space complexity: O(1)

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        ListNode vHead = new ListNode(0, head);
        ListNode cur = vHead;

        while (cur.next != null && cur.next.next != null) {
            int value = cur.next.val;
            // case: duplicate
            if (cur.next.next.val == value) {
                while (cur.next != null && cur.next.val == value) {
                    cur.next = cur.next.next;
                }
            }
            // case: not duplicate
            else cur = cur.next;
        }
        return vHead.next;
    }
}