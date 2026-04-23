# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class BSTIterator:
    # has/next TC - O(1) & SC - O(h)
    # Method 1: SC - O(h)
    # Push the leftmost path from root. Stack top = next smallest.
    # On pop, push the leftmost path of the popped node's right subtree.
    # The overall stack is in DESC order.
    def __init__(self, root):
        self.stack = []
        while root:
            self.stack.append(root)
            root = root.left
    
    def next(self):
        cur = self.stack.pop()
        node = cur.right
        while node:
            self.stack.append(node)
            node = node.left
        return cur.val
    
    def hasNext(self):
        return len(self.stack) > 0

    # # Method 2: SC - O(n)
    # def __init__(self, root: Optional[TreeNode]):
    #     def inorder(node):
    #         if not node: return
    #         inorder(node.left)
    #         self.record.append(node.val)
    #         inorder(node.right)
    #     self.record = []
    #     self.index = -1
    #     inorder(root)

    # def next(self) -> int:
    #     self.index += 1
    #     return self.record[self.index]

    # def hasNext(self) -> bool:
    #     return self.index + 1 < len(self.record)    


# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.next()
# param_2 = obj.hasNext()