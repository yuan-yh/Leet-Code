// 时间复杂度：O(Llogm)，其中 m 为 lists 的长度，L 为所有链表的长度之和。
// 空间复杂度：O(m)。堆中至多有 m 个元素。

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
    public ListNode mergeKLists(ListNode[] lists) {
        // 1. init a PQ
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);

        // 2. add all non-empty heads
        for (ListNode head : lists) {
            if (head != null) pq.offer(head);
        }
        // 3. record the smallest node & add if next
        ListNode vHead = new ListNode();
        ListNode cur = vHead, tmp;

        while (!pq.isEmpty()) {
            tmp = pq.poll();

            cur.next = tmp;
            cur = cur.next;

            if (tmp.next != null) pq.offer(tmp.next);
        }
        return vHead.next;
    }
}