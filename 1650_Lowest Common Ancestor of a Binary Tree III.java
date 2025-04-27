/*
// Definition for a Node.
class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
};
*/

// Method 1: hashset
class Solution {
    public Node lowestCommonAncestor(Node p, Node q) {
        if (p == q.parent)
            return p;
        if (q == p.parent)
            return q;
        if (p.parent == q.parent)
            return p.parent;

        HashSet<Node> set = new HashSet<>();

        while (p.parent != null) {
            set.add(p);
            p = p.parent;
        }

        while (q.parent != null && !set.contains(q)) {
            q = q.parent;
        }
        return q;
    }
}

// Method 2: align depth
/*
// Definition for a Node.
class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
};
*/

class Solution {
    public Node lowestCommonAncestor(Node p, Node q) {
        int pDepth = getDepth(p), qDepth = getDepth(q);

        Node deep = (pDepth >= qDepth) ? p : q;
        Node shallow = (pDepth < qDepth) ? p : q;
        int diff = Math.abs(pDepth - qDepth);

        while (diff > 0) {
            deep = deep.parent;
            diff--;
        }

        while (deep != shallow) {
            deep = deep.parent;
            shallow = shallow.parent;
        }
        return deep;
    }

    private int getDepth(Node n) {
        int depth = 0;
        while (n != null) {
            depth++;
            n = n.parent;
        }
        return depth;
    }
}