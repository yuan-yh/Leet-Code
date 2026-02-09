# IP 前缀匹配问题 — 用 Trie（前缀树）解决

## 题目理解

给定一组**前缀**（如 `*`, `192.168.*`, `192.168.2.*`, `192.168.2.1`）和一组 **IP 地址**，要求将每个 IP 匹配到**最长（最具体）的前缀**。如果没有任何前缀匹配，则匹配到通配符 `*`。

## 为什么用 Trie？

这道题的本质是**最长前缀匹配（Longest Prefix Match）**，这正是 Trie 的经典应用场景（路由器转发表就是这么做的）。

## 最优解思路

**1. 构建 Trie**

把每个前缀按 `.` 分割成段（token），逐段插入 Trie。例如：

```
*           →  根节点标记为匹配
192.168.*   →  根 → 192 → 168（标记为匹配）
192.168.2.* →  根 → 192 → 168 → 2（标记为匹配）
192.168.2.1 →  根 → 192 → 168 → 2 → 1（标记为匹配）
```

每个节点的 children 是一个 `HashMap<String, TrieNode>`，标记 `isEnd` 表示这里有一个合法前缀。

**2. 查询**

对每个 IP 地址，按 `.` 分割后沿 Trie 逐段向下走：
- 每经过一个标记为 `isEnd` 的节点，**记录当前匹配**（因为我们要最长匹配）
- 如果某一段在 children 中找不到，就停止
- 最终返回记录的**最后一次匹配**（即最长前缀）
- 如果一个都没匹配到，返回 `*`

## 代码示例（Python）

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.prefix = None  # 如果这里是一个合法前缀的终点，存储原始前缀字符串

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, prefix):
        node = self.root
        # 去掉末尾的 .* ，因为 * 代表"到此为止都匹配即可"
        parts = prefix.replace(".*", "").split(".")
        if prefix == "*":
            self.root.prefix = "*"
            return
        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        node.prefix = prefix  # 标记完整前缀

    def search(self, ip):
        node = self.root
        best_match = self.root.prefix  # 可能是 "*"
        parts = ip.split(".")
        for part in parts:
            if part in node.children:
                node = node.children[part]
                if node.prefix:
                    best_match = node.prefix  # 更新为更长的匹配
            else:
                break
        return best_match

# 使用
trie = Trie()
for p in ["*", "192.168.*", "192.168.2.*", "192.168.2.1"]:
    trie.insert(p)

ips = ["0.0.0.0", "192.168.7.1", "192.168.2.3", "192.168.2.1"]
for ip in ips:
    print(f"{ip} → {trie.search(ip)}")
```

**输出：**
```
0.0.0.0 → *
192.168.7.1 → 192.168.*
192.168.2.3 → 192.168.2.*
192.168.2.1 → 192.168.2.1
```

## 复杂度分析

| | 时间复杂度 |
|---|---|
| 插入一个前缀 | O(L)，L = 段数（最多4） |
| 查询一个 IP | O(L) |
| 总体 | O(N×L + M×L)，N = 前缀数，M = IP数 |

空间复杂度：O(N×L)，即 Trie 节点数。

## 关键点总结

- 这道题的核心考点就是识别出这是一个 **Longest Prefix Match** 问题
- Trie 是解决此类问题的标准数据结构
- 按 `.` 分割成段作为 Trie 的每一层（而不是按字符），这样更简洁高效
- `*` 作为全局默认匹配放在根节点即可