## 1Q1: financial service
A financial service company has required AWS...

Input: int[] security[n]; output: int minGroup
-	同组同级：同一个安全组中的所有服务器必须具有相同的安全等级 
-	组间平衡：任意两个安全组的服务器数量相差不能超过 1
Constraints: 1<= n, security[n] <=e5

```
def findMinimumGroups(security):
    from collections import Counter
    freq = Counter(security)
    frequencies = list(freq.values())
    n = len(security)
    
    def canAchieve(m):
        # Each group has size k or k+1
        k = n // m
        remainder = n % m  # number of groups with size k+1
        
        # We have 'remainder' groups of size (k+1) and (m - remainder) groups of size k
        total_groups = 0
        groups_of_k_plus_1 = 0
        
        for f in frequencies:
            if k == 0:
                # All groups must be size 1
                total_groups += f
                continue
            
            # For frequency f, min groups = ceil(f/(k+1)), max groups = floor(f/k)
            min_groups = (f + k) // (k + 1)  # ceil(f / (k+1))
            max_groups = f // k
            
            if min_groups > max_groups:
                return False
            
            # Greedy: use as few groups as possible (prefer larger groups)
            total_groups += min_groups
            # Count how many (k+1)-sized groups we're using
            groups_of_k_plus_1 += min_groups  # using all (k+1) sized initially
        
        return total_groups <= m
    
    # Binary search
    left, right = len(frequencies), n
    while left < right:
        mid = (left + right) // 2
        if canAchieve(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

## 2Q1: Amz distribution specialist
An amazon distribution specialist needs to process n packages...

Input: int[] center[i]; output: int minOperation
- 操作1：一次处理两个包裹 x 和 y，但前提是它们必须来自不同的配送中心（即 centers[x] != centers[y]）
- 操作2：一次处理一个包裹
```
import heapq
from collections import Counter

def min_operations(n, centers):
    # 统计每个中心的包裹数量
    freq = Counter(centers)
    
    # 构建最大堆（用负数模拟）
    max_heap = [-count for count in freq.values()]
    heapq.heapify(max_heap)
    
    operations = 0
    
    while len(max_heap) >= 2:
        # 取出最大的两个
        first = -heapq.heappop(max_heap)
        second = -heapq.heappop(max_heap)
        
        # 执行操作1，各减少1个包裹
        operations += 1
        first -= 1
        second -= 1
        
        # 如果还有剩余，放回堆中
        if first > 0:
            heapq.heappush(max_heap, -first)
        if second > 0:
            heapq.heappush(max_heap, -second)
    
    # 如果还剩一个中心的包裹，只能用操作2
    if max_heap:
        operations += -max_heap[0]
    
    return operations

# 测试示例
print(min_operations(5, [3, 7, 5, 6, 6]))  # 输出: 3
```

## 1Q2: scalable system
AWS provides scalable systems...

选择任意一个连续的子数组（区间） -> 将该区间内每台服务器的计算能力都增加x -> 找到使数组变成非递减顺序所需的最小操作总和（即所有x值的总和最小）。
```
def findMinimumSum(power):
    if not power or len(power) <= 1:
        return 0
    
    total = 0
    for i in range(1, len(power)):
        if power[i] < power[i - 1]:
            total += power[i - 1] - power[i]
    
    return total
```

## 2Q2: data infra team
As an engineer in Amazon's Data Infra Team...

streamCount个数据通道：每个数据通道需要连接到两个处理节点（一个作为主连接，一个作为副连接） -> 找出最大的总dataFlow，即所有数据通道的dataFlow之和的最大值。
```
"""
Maximum DataFlow Problem - Final Solution
时间复杂度: O(n log n log V)，其中 V 是带宽的最大值
空间复杂度: O(n)
"""

def determineMaxDataFlow(bandwidth, streamCount):
    n = len(bandwidth)
    if streamCount == 0:
        return 0
    
    # 1. 排序
    b = sorted(bandwidth)
    
    # 2. 前缀和（用于快速计算区间和）
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + b[i]
    
    def sum_range(l, r):
        """计算 b[l] 到 b[r] 的和"""
        if l > r:
            return 0
        return prefix[r + 1] - prefix[l]
    
    def count_and_sum_geq(threshold):
        """
        计算所有满足 b[i] + b[j] >= threshold 的有序对 (i,j) 的数量和总和
        使用二分查找优化
        """
        total_sum = 0
        count = 0
        
        for j in range(n):
            # 找最小的 i 使得 b[i] + b[j] >= threshold
            # 即 b[i] >= threshold - b[j]
            need = threshold - b[j]
            
            # 二分查找
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if b[mid] >= need:
                    hi = mid
                else:
                    lo = mid + 1
            
            # 所有 i 从 lo 到 n-1 都有效
            num_valid = n - lo
            if num_valid > 0:
                count += num_valid
                # 贡献: sum(b[lo:n]) + num_valid * b[j]
                total_sum += sum_range(lo, n - 1) + num_valid * b[j]
        
        return count, total_sum
    
    # 3. 二分查找阈值 T
    # 找最大的 T 使得 count(sum >= T) >= streamCount
    lo = 2 * b[0]
    hi = 2 * b[n - 1] + 1
    
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cnt, _ = count_and_sum_geq(mid)
        if cnt >= streamCount:
            lo = mid
        else:
            hi = mid - 1
    
    threshold = lo
    
    # 4. 计算结果
    # 分别计算 sum > T 和 sum >= T 的情况
    count_gt, sum_gt = count_and_sum_geq(threshold + 1)
    
    # 需要从 sum = threshold 的对中取多少个
    need_from_eq = streamCount - count_gt
    
    # 结果 = (sum > T 的所有对的和) + (需要的 sum = T 的对数) * T
    result = sum_gt + need_from_eq * threshold
    
    return result


# ============ 测试代码 ============
if __name__ == "__main__":
    # 题目示例
    print("=" * 50)
    print("题目示例: bandwidth = [6, 4, 7], streamCount = 4")
    print("预期输出: 52")
    print("实际输出:", determineMaxDataFlow([6, 4, 7], 4))
    print()
    
    # 验证示例的计算过程
    print("验证:")
    print("排序后: [4, 6, 7]")
    print("所有9个节点对的和:")
    b = sorted([6, 4, 7])
    pairs = []
    for i in range(3):
        for j in range(3):
            pairs.append((b[i], b[j], b[i] + b[j]))
    pairs.sort(key=lambda x: -x[2])
    for i, (x, y, s) in enumerate(pairs):
        mark = " <-- 选择" if i < 4 else ""
        print(f"  ({x}, {y}) = {s}{mark}")
    print(f"前4大的和: {sum(p[2] for p in pairs[:4])}")
```

## 3Q2: work on algo
The developers at Amazon are working on an algo for their data distribution...

Given n / affinity
```
"""
最大亲和度问题 - 数据分配到两个区域

解题思路:
1. 将规则看作图的边，数据看作节点
2. 用DFS找连通分量并二分图染色
3. 用DP在满足"A选n/2个"约束下最大化A的总和
"""

def maximumAffinity(affinity, rules):
    """
    计算regionA能获得的最大亲和度总和
    
    参数:
        affinity: List[int] - 长度为n的数组，affinity[i]表示第i+1个数据的亲和度
        rules: List[List[int]] - m个规则，每个规则[x,y]表示索引x和y的约束(1-indexed)
    
    返回:
        int - regionA的最大可能亲和度总和
    """
    n = len(affinity)
    
    # 步骤1: 建图 (使用1-indexed，与题目一致)
    graph = [[] for _ in range(n + 1)]
    for rule in rules:
        x, y = rule[0], rule[1]
        graph[x].append(y)
        graph[y].append(x)
    
    # 步骤2: 找所有连通分量并二分图染色
    visited = [False] * (n + 1)
    components = []  # 存储每个连通分量的两个分组
    
    for i in range(1, n + 1):
        if visited[i]:
            continue
        
        # DFS染色，分成group0和group1
        group0, group1 = [], []
        stack = [(i, 0)]  # (节点, 颜色)
        
        while stack:
            node, color = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            
            # 根据颜色分组（注意affinity是0-indexed）
            if color == 0:
                group0.append(affinity[node - 1])
            else:
                group1.append(affinity[node - 1])
            
            # 邻居染相反颜色
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    stack.append((neighbor, 1 - color))
        
        components.append((group0, group1))
    
    # 步骤3: 动态规划
    # dp[j] = A选了j个数据时的最大亲和度总和
    target = n // 2  # A需要恰好选n/2个
    dp = {0: 0}
    
    for group0, group1 in components:
        sum0, cnt0 = sum(group0), len(group0)
        sum1, cnt1 = sum(group1), len(group1)
        new_dp = {}
        
        for j, val in dp.items():
            # 方式1: group0 分给 A
            if j + cnt0 <= target:
                key = j + cnt0
                new_dp[key] = max(new_dp.get(key, float('-inf')), val + sum0)
            
            # 方式2: group1 分给 A
            if j + cnt1 <= target:
                key = j + cnt1
                new_dp[key] = max(new_dp.get(key, float('-inf')), val + sum1)
        
        dp = new_dp
    
    return dp.get(target, 0)


# ==================== 测试代码 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("Maximum Affinity 测试")
    print("=" * 60)
    
    # 样例1: 来自题目
    # n=4, affinity=[1,2,3,4], rules=[[4,2]]
    # 最优: A选索引4和3的数据(值4和3)，总和=7
    result1 = maximumAffinity([1, 2, 3, 4], [[4, 2]])
    print(f"样例1: {result1} (期望: 7)")
    assert result1 == 7, f"样例1失败: 得到{result1}, 期望7"
    
    # 样例2: 来自题目详细例子
    # n=6, affinity=[3,2,-4,8,3,-7], rules=[[2,4],[3,6]]
    # A选: -4, 8, 3 -> 总和 = 7
    result2 = maximumAffinity([3, 2, -4, 8, 3, -7], [[2, 4], [3, 6]])
    print(f"样例2: {result2} (期望: 7)")
    assert result2 == 7, f"样例2失败: 得到{result2}, 期望7"
    
    # 测试3: 无规则
    result3 = maximumAffinity([1, 2, 3, 4], [])
    print(f"测试3 (无规则): {result3} (期望: 7)")
    assert result3 == 7
    
    # 测试4: 全部配对
    result4 = maximumAffinity([1, 2, 3, 4], [[1, 2], [3, 4]])
    print(f"测试4 (全配对): {result4} (期望: 6)")
    assert result4 == 6
    
    # 测试5: 链式规则
    result5 = maximumAffinity([1, 10, 2, 20], [[1, 2], [2, 3]])
    print(f"测试5 (链式): {result5} (期望: 30)")
    assert result5 == 30
    
    # 测试6: 全负数
    result6 = maximumAffinity([-1, -2, -3, -4], [])
    print(f"测试6 (负数): {result6} (期望: -3)")
    assert result6 == -3
    
    print()
    print("✓ 所有测试通过!")
    print("=" * 60)
```

## 4Q2: testing a modified algo
Developers at Amazon are testing a modified algo...字符串排序
```
"""
问题描述：
给定一个字符串 strValue，找出将该字符串排序成有序状态所需的最少操作次数。
每次操作可以选择任意一个真子串（proper substring，不能是整个字符串），对其进行排序。

解题思路：
1. 如果字符串已经有序 → 0次
2. 如果首字符是全局最小 或 末字符是全局最大 → 1次
   - 因为可以排序除该字符外的部分，一次完成
3. 如果前n-1个字符包含全局最小 或 后n-1个字符包含全局最大 → 2次
   - 第一次排序把最小/最大字符移到正确位置
   - 第二次排序完成剩余部分
4. 否则（全局最小只在末尾，全局最大只在开头）→ 3次
   - 需要额外一次操作来打破这种"最坏"的初始配置

时间复杂度：O(n) 用于找最小/最大字符
空间复杂度：O(n) 用于排序后的字符串（可优化为O(1)）
"""


def minOperations(strValue: str) -> int:
    """
    计算将字符串排序所需的最少操作次数。
    
    Args:
        strValue: 输入字符串
        
    Returns:
        最少操作次数（0, 1, 2, 或 3）
        如果长度为2且未排序，返回-1（无法排序）
    """
    n = len(strValue)
    
    # 边界情况：空串或单字符
    if n <= 1:
        return 0
    
    # 获取排序后的字符串
    sorted_str = ''.join(sorted(strValue))
    
    # 情况0：字符串已经有序
    if strValue == sorted_str:
        return 0
    
    # 特殊情况：长度为2且未排序（真子串只能是单个字符，排序无意义）
    if n == 2:
        return -1
    
    # 获取全局最小和最大字符
    min_char = sorted_str[0]
    max_char = sorted_str[-1]
    
    # 情况1：首字符已是最小 或 末字符已是最大 → 1次操作
    if strValue[0] == min_char or strValue[-1] == max_char:
        return 1
    
    # 情况2：检查能否通过2次操作完成
    # 条件：前n-1个字符包含全局最小 或 后n-1个字符包含全局最大
    if min(strValue[:-1]) == min_char or max(strValue[1:]) == max_char:
        return 2
    
    # 情况3：全局最小只在末尾，全局最大只在开头 → 3次操作
    return 3


# ============== 以下为测试代码 ==============

def test():
    """运行测试用例"""
    test_cases = [
        ("zyxpqa", 3),   # 题目示例
        ("abc", 0),      # 已排序
        ("cba", 3),      # 完全逆序
        ("acb", 1),      # 首字符是最小
        ("bca", 2),      # 后两个包含最大
        ("bac", 1),      # 末字符是最大
        ("cab", 2),      # 前两个包含最小
        ("dcba", 3),     # 完全逆序
        ("a", 0),        # 单字符
        ("", 0),         # 空串
        ("ba", -1),      # 长度2无法排序
    ]
    
    print("测试结果：")
    print("-" * 40)
    
    all_pass = True
    for s, expected in test_cases:
        result = minOperations(s)
        status = "✓" if result == expected else "✗"
        print(f"{status} minOperations('{s}') = {result} (期望: {expected})")
        if result != expected:
            all_pass = False
    
    print("-" * 40)
    if all_pass:
        print("✓ 所有测试通过！")
    else:
        print("✗ 有测试失败")


if __name__ == "__main__":
    test()
```

## 5Q2: manager of amz warehouse
```
"""
Amazon Warehouse Price Adjustment - Minimum Operations

Algorithm: Greedy + Enumeration of Target Ranges

Time Complexity: O(n² log n) - O(n) candidates × O(n) evaluation each
Space Complexity: O(n)
"""

from typing import List


def minOperations(n: int, prices: List[int], k: int, d: int) -> int:
    """
    Find minimum operations to make max(prices) - min(prices) < d.
    
    Each operation:
    - Select indices x, y and value p (1 ≤ p ≤ k)
    - Increase prices[x] by p
    - Decrease prices[y] by p
    
    Args:
        n: Number of products
        prices: Array of product prices (1-indexed in problem, 0-indexed here)
        k: Maximum adjustment per operation
        d: Target maximum difference (strictly less than)
    
    Returns:
        Minimum number of operations needed
    """
    if not prices:
        return 0
    
    prices = sorted(prices)
    
    # Already satisfied
    if prices[-1] - prices[0] < d:
        return 0
    
    def calc_ops(L: int) -> int:
        """Calculate operations for target range [L, L+d-1]"""
        R = L + d - 1
        inc = sum((L - p + k - 1) // k for p in prices if p < L)
        dec = sum((p - R + k - 1) // k for p in prices if p > R)
        return max(inc, dec)  # Each op does both increase and decrease
    
    # Optimal L aligns with some price or price-(d-1)
    candidates = {p for p in prices} | {p - d + 1 for p in prices}
    
    return min(calc_ops(L) for L in candidates)


# Example usage
if __name__ == "__main__":
    # Example from problem: n=4, prices=[1,5,9,11], k=4, d=2
    print(minOperations(4, [1, 5, 9, 11], 4, 2))  # Output: 3
```

## 6Q2: part of amz’s network infra division
```
import heapq

def maxBandwidthRate(capacity, connectionCount):
    n = len(capacity)
    if connectionCount == 0:
        return 0
    
    # Create indices sorted by capacity in descending order
    sorted_indices = sorted(range(n), key=lambda x: capacity[x], reverse=True)
    
    # Max heap: store (-sum, rank_i, rank_j) where rank refers to position in sorted order
    max_heap = []
    
    # Start with the best pair: (largest, largest)
    best_cap = capacity[sorted_indices[0]]
    heapq.heappush(max_heap, (-2 * best_cap, 0, 0))
    
    visited = {(0, 0)}
    total = 0
    
    for _ in range(connectionCount):
        neg_sum, ri, rj = heapq.heappop(max_heap)
        total += -neg_sum
        
        # Add neighbors: (ri+1, rj) and (ri, rj+1)
        if ri + 1 < n and (ri + 1, rj) not in visited:
            new_sum = capacity[sorted_indices[ri + 1]] + capacity[sorted_indices[rj]]
            heapq.heappush(max_heap, (-new_sum, ri + 1, rj))
            visited.add((ri + 1, rj))
        
        if rj + 1 < n and (ri, rj + 1) not in visited:
            new_sum = capacity[sorted_indices[ri]] + capacity[sorted_indices[rj + 1]]
            heapq.heappush(max_heap, (-new_sum, ri, rj + 1))
            visited.add((ri, rj + 1))
    
    return total
```

## 7Q2: Amz games
```
"""
Amazon Tournament Problem - Power Boosters

Problem: Find the number of players who can defeat all other players.
X can defeat Y if there exists an arrangement where X wins at least 2 out of 3 rounds.

Time Complexity: O(n²) where n is the number of players
Space Complexity: O(n) for storing player boosters

Key Insight:
For sorted arrays x1 < x2 < x3 and y1 < y2 < y3,
X can defeat Y if and only if: x2 > y1 AND x3 > y2

This is because:
- x2 > y1 means x2 can beat y1, and x3 can beat y1
- x3 > y2 means x3 can beat y2 (and y1)
- Combined: we can assign x2 -> y1 (win) and x3 -> y2 (win) = 2 wins
"""


def can_defeat(x, y):
    """
    O(1) check if player X can defeat player Y.
    
    X defeats Y if there EXISTS arrangements of X and Y where X wins >= 2 rounds.
    
    For sorted arrays x1 < x2 < x3 and y1 < y2 < y3:
    X can defeat Y iff x2 > y1 AND x3 > y2
    """
    xs = sorted(x)
    ys = sorted(y)
    return xs[1] > ys[0] and xs[2] > ys[1]


def count_dominant_players(boosters):
    """
    Count players who can defeat all other players.
    
    Args:
        boosters: List of [a, b, c] where each is a player's 3 power boosters
    
    Returns:
        Number of players who can defeat all other players
    """
    n = len(boosters)
    count = 0
    
    for i in range(n):
        can_defeat_all = True
        for j in range(n):
            if i != j and not can_defeat(boosters[i], boosters[j]):
                can_defeat_all = False
                break
        if can_defeat_all:
            count += 1
    
    return count


def solve(n, booster_a, booster_b, booster_c):
    """
    Main solution function.
    
    Args:
        n: Number of players
        booster_a: List of first boosters for each player
        booster_b: List of second boosters for each player  
        booster_c: List of third boosters for each player
    
    Returns:
        Number of players who can defeat all other players
    """
    players = [[booster_a[i], booster_b[i], booster_c[i]] for i in range(n)]
    return count_dominant_players(players)


# Example usage and test
if __name__ == "__main__":
    # Problem example
    n = 3
    booster_a = [9, 4, 2]
    booster_b = [5, 12, 10]
    booster_c = [11, 3, 13]
    
    result = solve(n, booster_a, booster_b, booster_c)
    print(f"Number of players who can defeat all others: {result}")
    # Expected output: 2 (Players 1 and 3)
```

## 8Q2: A PM is assigning a series
```
"""
Task Scheduling - Minimum Effort Sum
====================================
Problem: 
- n tasks with effort levels, must be completed in order
- Complete all tasks within 'deadline' days
- Each day must have at least one task
- Day's effort = max effort of tasks on that day
- Minimize: sum of all days' efforts

Solution: Dynamic Programming
Time: O(n² * deadline) 
Space: O(n * deadline), can be optimized to O(n)
"""

def getMinEffort(efforts: list[int], deadline: int) -> int:
    """
    Main solution using Dynamic Programming.
    
    State: dp[i][j] = min total effort to complete first i tasks in j days
    Transition: dp[i][j] = min(dp[k][j-1] + max(efforts[k:i])) for valid k
    """
    n = len(efforts)
    
    # Edge cases
    if deadline >= n:
        return sum(efforts)  # Each task gets its own day
    if deadline == 1:
        return max(efforts)  # All tasks in one day
    
    INF = float('inf')
    
    # Precompute range maximums: max_val[i][j] = max(efforts[i:j+1])
    max_val = [[0] * n for _ in range(n)]
    for i in range(n):
        max_val[i][i] = efforts[i]
        for j in range(i + 1, n):
            max_val[i][j] = max(max_val[i][j-1], efforts[j])
    
    # DP with space optimization (rolling array)
    # prev[i] = min effort to complete first i tasks in (current_day - 1) days
    prev = [INF] * (n + 1)
    prev[0] = 0
    
    # Base case: 1 day
    running_max = 0
    for i in range(1, n + 1):
        running_max = max(running_max, efforts[i - 1])
        prev[i] = running_max
    
    # Fill for days 2 to deadline
    for day in range(2, deadline + 1):
        curr = [INF] * (n + 1)
        
        for i in range(day, n + 1):  # Need at least 'day' tasks for 'day' days
            # Try splitting: first k tasks in (day-1) days, tasks k+1..i on last day
            last_day_max = 0
            for k in range(i, day - 1, -1):  # k from i down to day-1
                last_day_max = max(last_day_max, efforts[k - 1])
                if prev[k - 1] < INF:
                    curr[i] = min(curr[i], prev[k - 1] + last_day_max)
        
        prev = curr
    
    return prev[n]


def getMinEffort_2D(efforts: list[int], deadline: int) -> int:
    """
    Standard 2D DP version (easier to understand).
    """
    n = len(efforts)
    
    if deadline >= n:
        return sum(efforts)
    if deadline == 1:
        return max(efforts)
    
    INF = float('inf')
    
    # dp[i][j] = min effort for first i tasks in j days
    dp = [[INF] * (deadline + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, min(i, deadline) + 1):
            # Compute max for last day's tasks on the fly
            last_day_max = 0
            for k in range(i, j - 1, -1):  # Last day does tasks k to i
                last_day_max = max(last_day_max, efforts[k - 1])
                if dp[k - 1][j - 1] < INF:
                    dp[i][j] = min(dp[i][j], dp[k - 1][j - 1] + last_day_max)
    
    return dp[n][deadline]


# ============== Test ==============
if __name__ == "__main__":
    # Example: efforts = [1, 2, 3, 4, 5], deadline = 3
    # Optimal: [1] + [2] + [3,4,5] = 1 + 2 + 5 = 8
    
    print("=" * 50)
    print("Task Scheduling - Minimum Effort Sum")
    print("=" * 50)
    
    efforts = [1, 2, 3, 4, 5]
    deadline = 3
    
    result = getMinEffort(efforts, deadline)
    print(f"\nInput: efforts = {efforts}, deadline = {deadline}")
    print(f"Output: {result}")
    print(f"Expected: 8")
    print(f"Explanation: Day1=[1]→1, Day2=[2]→2, Day3=[3,4,5]→5, Total=8")
    
    # More tests
    print("\n" + "-" * 50)
    print("Additional Test Cases:")
    print("-" * 50)
    
    tests = [
        ([5, 4, 3, 2, 1], 3, 8),
        ([1, 1, 1, 1, 1], 3, 3),
        ([10, 1, 1, 1, 1], 2, 11),
        ([1, 1, 1, 1, 10], 2, 11),
        ([3, 1, 4, 1, 5, 9, 2, 6], 4, 17),
        ([7, 2, 5, 10, 8], 2, 17),  # [7,2,5] + [10,8] = 7+10=17 or [7]+[2,5,10,8]=7+10=17
    ]
    
    for efforts, deadline, expected in tests:
        result = getMinEffort(efforts, deadline)
        status = "✓" if result == expected else "✗"
        print(f"{status} efforts={efforts}, deadline={deadline} → {result} (expected {expected})")
```