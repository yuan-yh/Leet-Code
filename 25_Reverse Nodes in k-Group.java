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
    public ListNode reverseKGroup(ListNode head, int k) {
        // 1. iterate to get LL-length
        int length = 0;
        ListNode tmp = head;
        while (tmp != null) {
            tmp = tmp.next;
            length ++;
        }

        // edge case: len = 1 || k = 1
        if (length == 1 || k == 1) return head;

        // 2. reverse x times (then append rest)
        ListNode vHead = new ListNode(0, head);
        ListNode leftwards = vHead, left = head, cur = head, prev = null;
        int reverse = length / k, count;

        for (int i = 0; i < reverse; i++) {
            count = 0;
            while (count < k) {
                tmp = cur.next;
                cur.next = prev;
                prev = cur;
                cur = tmp;
                count ++;
            }
            leftwards.next = prev;
            left.next = cur;

            leftwards = left;
            left = cur;
            prev = null;
        }

        return vHead.next;
    }
}