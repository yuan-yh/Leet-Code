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
    public ListNode swapPairs(ListNode head) {
        // edge case: null or one node only
        if (head == null || head.next == null) return head;

        ListNode vHead = new ListNode(0, head);
        // iterate through and swap for each pair
        ListNode leftwards = vHead, prev = null, cur = vHead.next, next, tmp;

        while (cur != null && cur.next != null) {
            next = cur.next;
            tmp = next.next;
            // swap
            leftwards.next = next;
            next.next = cur;
            cur.next = tmp;
            // update
            leftwards = cur;
            cur = tmp;
        }

        return vHead.next;
    }
}