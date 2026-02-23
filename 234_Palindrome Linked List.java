// 时间复杂度：O(n)，其中 n 是链表的长度（节点个数）。
// 空间复杂度：O(1)。

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
        ListNode slow = head, fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    private ListNode reverse(ListNode head) {
        ListNode cur = head, prev = null, tmp;

        while (cur != null) {
            tmp = cur.next;
            cur.next = prev;
            prev = cur;
            cur = tmp;
        }

        return prev;
    }

    public boolean isPalindrome(ListNode head) {
        // 1. find middle
        ListNode mid = findMiddle(head);

        // 2. reverse middle afterwards, now both left/right's tail pointed to the middle
        ListNode p2 = reverse(mid);

        // 3. compare
        ListNode p1 = head;
        while (p2 != null) {
            if (p1.val != p2.val) return false;
            p1 = p1.next;
            p2 = p2.next;
        }
        return true;
    }
}