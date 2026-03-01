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
    private ListNode findMiddle(ListNode head) {
        ListNode slow = head, fast = head, prev = null;

        while (fast != null && fast.next != null) {
            prev = slow;
            slow = slow.next;
            fast = fast.next.next;
        }
        prev.next = null;
        return slow;
    }

    private ListNode merge(ListNode left, ListNode right) {
        ListNode vHead = new ListNode();
        ListNode cur = vHead;

        while (left != null && right != null) {
            if (left.val < right.val) {
                cur.next = left;
                left = left.next;
            } else {
                cur.next = right;
                right = right.next;
            }
            cur = cur.next;
        }

        cur.next = (left != null) ? left : right;
        return vHead.next;
    }

    public ListNode sortList(ListNode head) {
        // 1. case: <= 1 node
        if (head == null || head.next == null) return head;

        // 2. divide: split into two halves
        ListNode right = findMiddle(head);
        ListNode left = head;

        // 3. sort
        left = sortList(left);
        right = sortList(right);

        // 4. merge / conquer
        return merge(left, right);
    }
}