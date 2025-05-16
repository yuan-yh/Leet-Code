## Amazon Summer Intern
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

## TikTok Summer Intern
### vo 1
25min resume (work experience *metric calculation)

15min LC14: https://leetcode.com/problems/longest-common-prefix/description/

ArrayList和LinkedList
静态变量和实例变量
final, finally 和 finalize 的区别
死锁以及如何避免
单例模式 (Singleton) + coding sample

### vo 2
30min resume (2 projects - *sql分表 & test coverage)

Java反射
依赖倒置 / 控制反转 / 依赖注入
Python装饰器

Coding: 写一个计算并打印函数执行时间的装饰器
Coding: 打印钻石, 描述test case
Coding: SQL - 成绩表（挑出所有没有挂科的学生的信息）
    ```
    题目描述如下：

    表名：student_profile

    字段：id, name, sex, discipline, grade

    示例数据：
    1,zhangsan,male,Chinese,30
    1,zhangsan,male,Math,60
    2,lisi,male,Chinese,70
    2,lisi,male,Math,80
    要求： 挑出所有没有挂科的学生的信息。
    （挂科通常是指成绩低于 
    ```