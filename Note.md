Given the input binary tree find the mirror image of the given tree, and do it in place?


Input:
 5
 / \
7   8
/
9



Output:
 5
 / \
8   7
     \
      9

class Node {
    int val;
    Node left;
    Node right;
    
    Node (int x) {this.val = x;}
}

class Solution {
    public Node mirror (Node root) {
        // edge case: root is null
        if (root == null) return null;
        
        // switch
        Node left = root.left;
        root.left = root.right;
        root.right = left;
        // process
        mirror(root.left);
        mirror(root.right);
        
        return root;
    }
}

there are multiple storage nodes int[]
1 coordinate talk to those storage nodes
find the min / max / sum / mean(avg) / median

N - No. of Storage nodes
M - No. of elements in each of the storage nodes

The Space complexity is O(N * M)

class Storage {
    int[] list;
    
    //You can define any method you want
    public Long getSum() {
        Long sum = 0;
        for (int i : list) sum += i;
        return sum;
    }
    
    public int getMin() {
        int min = list[0];
        for (int i : list) min = Math.min(min, i);
        return min;
    }

}

class Solution {
    public Long mean(List<Storage> storages) {
        // List<Integer> count = new ArrayList<>();
        Long sum = 0, size = 0;Integer.MAX_VALU
        for (int i = 0; i < storages.size(); i++) {
            sum += storages.get(i).getSum();
            size += storages.get(i).size();
        }
        
        // edge case: empty storages
        if (size == 0) threw new IllegalException();
        
        Long mean = sum / size;
        return mean;
    }
    
    public Long min(List<Storage> storages) {
        int min = Integer.MAX_VALUE;
        for (int i = 0; i < storages.size(); i++) {
            min = Math.min(min, storages.get(i).getMin());
        }
        return min;
    }
}