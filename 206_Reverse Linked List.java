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

// Method 1: reverse iteratively：O(n)
class Solution {
    public ListNode reverseList(ListNode head) {
        // 1 -> 2 -> null // reverse: null <- 1 <- 2
        // add connection: 'null <- 1' and break connection '1 -> 2'
        ListNode cur = head, prev = null, tmp;

        while (cur != null) {
            tmp = cur.next;
            cur.next = prev;
            prev = cur;
            cur = tmp;
        }

        return prev;
    }
}