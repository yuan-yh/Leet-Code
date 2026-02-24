// 时间复杂度：O(n+m)，其中 n 为 list1的长度，m 为 list2的长度。
// 空间复杂度：O(1)。仅用到若干额外变量。

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
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        // 1. short-cut
        if (l2 == null) return l1;

        // 2. assign l1 a virtual head
        ListNode vHead = new ListNode(0, l1);
        ListNode cur = vHead, tmp;

        // 3. loop to merge l2
        while (l2 != null) {
            // case: empty l1 || l1.val VS l2.val
            if (cur.next == null) {
                cur.next = l2;
                break;
            }
            if (cur.next.val > l2.val) {
                tmp = l2.next;
                l2.next = cur.next;
                cur.next = l2;
                l2 = tmp;
            }
            cur = cur.next;
        }
        return vHead.next;
    }
}