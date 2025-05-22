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

// Method 1: iteration
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

// Method 2: recursion
// 时间复杂度：O(n)，其中 n 为链表长度。
// 空间复杂度：O(n)
class Solution {
    public ListNode swapPairs(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }

        ListNode node1 = head;
        ListNode node2 = head.next;
        ListNode node3 = node2.next;

        node1.next = swapPairs(node3); // 1 指向递归返回的链表头
        node2.next = node1; // 2 指向 1

        return node2; // 返回交换后的链表头节点
    }
}