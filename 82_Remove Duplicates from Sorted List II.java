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
        ListNode prev = vHead, cur = head;

        while (cur != null && cur.next != null) {
            if (cur.val == cur.next.val) {
                // find the next node dif from cur, then cut all cur nodes
                while (cur.next != null && cur.val == cur.next.val) cur = cur.next;
                prev.next = cur.next;
            }
            else prev = prev.next;
            cur = cur.next;
        }

        return vHead.next;
    }
}