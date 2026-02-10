# 面试题解析

## 题目1：给定数组，将每个元素翻倍后追加到数组末尾，然后打乱顺序

例如：`[1,4]` → `[1,4,2,8]` → `[2,1,4,8]`

这题比较直接：

```python
import random

def double_and_shuffle(arr):
    doubled = arr + [x * 2 for x in arr]
    random.shuffle(doubled)
    return doubled
```

时间复杂度 O(n)，空间复杂度 O(n)。没什么难点。

---

## Follow Up（重点）：给定打乱后的数组，还原原始数组

例如：`[2,1,4,8]` → `[1,4]`

这才是面试的核心考点。

### 思路

关键观察：**原始数组中最小的元素，翻倍后的值也一定在数组中。** 所以我们可以用贪心 + 排序的方法：

1. 把打乱后的数组排序
2. 用一个 multiset / counter 来追踪哪些元素还可用
3. 从最小的元素开始遍历：如果这个元素还没被"消耗"掉，它一定属于原始数组，然后把它的两倍从 counter 中移除（因为那是它对应的翻倍值）

### 为什么贪心是对的？

排序后从小到大处理，最小的未使用元素**不可能**是别人的翻倍值（因为比它小的都处理完了），所以它一定是原始元素。

### 代码

```python
from collections import Counter

def find_original(changed):
    changed.sort()
    count = Counter(changed)
    original = []
    
    for num in changed:
        if count[num] == 0:
            continue
        # num 属于原始数组
        count[num] -= 1
        # 它的翻倍值必须存在
        if count[num * 2] == 0:
            return []  # 无效输入
        count[num * 2] -= 1
        original.append(num)
    
    return original
```

### 复杂度

- 时间：**O(n log n)**（排序主导）
- 空间：**O(n)**（Counter）

### 需要注意的边界情况

- 数组长度必须是偶数，否则直接返回空
- 包含 **0** 的情况：0 * 2 = 0，所以 0 必须成对出现
- 无效输入（找不到对应翻倍值）

这道题对应的是 LeetCode 2007 "Find Original Array From Doubled Array"（帖子里说的"二玲玲期"就是 2007）。