## Part 2: Object-Oriented Design (OOD)

| # | Topic | Count |
|---|-------|-------|
| 1 | **Rate Limiter** | 2 |
其实面ood的时候，多种写法都应该主动讨论一下，rate limiter我主动说了几种解法，并分别讨论了优劣和适用范围
最后就说在这个题的背景下我觉得xxx比较好

| 2 | **LRU / LFU Cache** | LC 146, 460 | 4 |
LFU cache是用的OrderedDict 还是自己去定义的双向链表啊 lru 不用ordereddict可以理解 flu也自己定义双向链表吗 自己定义 好 双向链

| 3 | **Log Parsing / Processing** — Parse logs, find common entries across logs, brute force | LC 560 variant, custom | 3 |
log处理（两份log，找到同时出现在两个log里and浏览了不同的网站的人）
similar to LC635, with timestamp

给定一长串log, 然后要去找log里面的内容
一开始没想bruce force, 我先跟他讨论我的approach 讨论完才开始写
讨论到一半说可以线段树做 但会写不完 我BQ完只剩25分钟coding吧

修日志是在日志里找他家那个服务器坏了

| 3 | **Hit Counter** | 1 |
| 4 | **TinyURL** | 1 |
| 5 | **Time-Based Key-Value Store** | 1 |
| 6 | **Trie** | 1 |
| 7 | **Design Twitter** (renamed to Design Facebook but same problem; BFS/DFS + Union Find follow-up) | 1 |
design推特名字改成设计facebook实际还是设计推特 followup问了推特找朋友实际上就是bfs dfs。快速找朋友union find

| 8 | **Movie Lookup by Date** (return movie on a given date, or nearest date) | 1 |
| 9 | **File Parser** — Read file and output JSON | 1 |
| 10 | **Locker System** — Given dimensions, find the smallest-volume locker that fits | 1 |
| 11 | **Time Tracker** | 1 |
| 12 | **Design HashMap** | LC 706 | 1 |
| 13 | **Voting System** — OOD for a voting / election mechanism | 1 |

---
## Part 1: Coding / Algorithm Questions
ListNode.__lt__ = lambda self, other : (self.val < other.val)

### Tier 1: Very High Frequency

| # | Topic | Related LeetCode | Count |
|---|-------|-----------------|-------|
| 1 | **Island Problems / DFS / BFS / Union Find / Clone Graph** — Connected components, max island area, graph traversal, clone graph | LC 200, 695, 684, 547, 721, 133 | 10 |
| 2 | **Top K Elements** — Find k-th largest, top k frequent, kth smallest in BST | LC 215, 347, *230* | 7 |
| 3 | **Course Schedule (Topological Sort)** — Variants, log-file input variants | LC 207, 210 | 6 |
Course schedule加了amazon背景 follow up return all cycles 

| 7 | **Polish Notation / Expression Tree** — Evaluate or build expression tree | LC 1628, 1597, 150 | 3 |
| 5 | House Robber / DP on Arrays — Cannot rob adjacent, **tree DP variants** | LC 198, 213 | 3 |
| 6 | Clone Linked List with Random Pointer | LC 138 | 3 |
| 9 | Merge Sorted Arrays / Lists — Merge two sorted arrays, merge k sorted lists | LC 88, 23 | 3 |
| 10 | **Word Find** |  |  |
union find(684，547，721?)

### Tier 2: High Frequency

| # | Topic | Related LeetCode | Count |
|---|-------|-----------------|-------|
| 11 | **Sliding Window Maximum** | LC 239 | 2 |
| 12 | **Jump Game** | LC 55, 45 | 2 |
| 13 | **Meeting Room / Interval Scheduling** — Max events, interval greedy | LC 252, 253, 1353 | 2 |
| 15 | **Trapping Rain Water** | LC 42 | 2 |
| 16 | **Word Break / Concatenated Words** — 1D DP, hard variants | LC 139, 140, 472 | 2 |
| 17 | **Tree Traversal** — Inorder (iterative + recursive), postorder; OS-level follow-ups on stack overflow | LC 94, 145 | 2 |
| 18 | **Anagram / String Reorganization** — Anagram variant, reorganize string | LC 49 variant, 767 | 2 |
| 46 | OOD Version - Rotten Oranges (BFS) | LC 994 | 2 |

### Tier 3: Mentioned Once

| # | Topic | Related LeetCode | Count |
|---|-------|-----------------|-------|
| 19 | Valid Parentheses (with noise characters) | LC 20 variant | 1 |
| 20 | LC 329 — Longest Increasing Path in a Matrix | LC 329 | 1 |
| 21 | LC 270 — Closest Binary Search Tree Value | LC 270 | 1 |
| 22 | LC 56 — Merge Intervals | LC 56 | 1 |
| 23 | Climbing Stairs (DP) + Space Optimization follow-up | LC 70 | 1 |
| 24 | Compare Version Number — Variant | LC 165 | 1 |
| 25 | Broken Calculator + Cache Variant | LC 991 | 1 |
就是input是n 和 m, 按红色的按钮会将n * 2, 按蓝色的按钮会将n - 1. find the minimum number of time that you have to click the buttons to achieve m
我用的bfs, 然后time complexity space complexity也说对了

| 26 | LC 4 — Median of Two Sorted Arrays (Hard variant) | LC 4 | 1 |
| 27 | LC 383 — Ransom Note | LC 383 | 1 |
| 28 | Buy and Sell Stock | LC 121 | 1 |
| 29 | String Compression | LC 443 | 1 |
| 30 | Lowest Common Ancestor | LC 236 | 1 |
| 31 | Trie / String Matching | LC 208 | 1 |
| 32 | Counting Duplicate IDs (with streaming follow-up) | — | 1 |
| 33 | Water Flow Shortest Path | — | 1 |
| 34 | Raindrops on Sidewalk (non-LC, Google-style) | — | 1 |
| 35 | Stack Implementation | — | 1 |
| 36 | LC 510 + LC 2215 | LC 510, 2215 | 1 |
| 37 | Scenario-based problem (dictionary + heap, O(1) constraint) | — | 1 |
| 38 | LC 2918 — Minimum Equal Sum of Two Arrays After Replacing Zeros | LC 2918 | 1 |
| 40 | Supply Chain Profit on Tree — Custom tree DP with LCA and transit fees | Custom (tree DP) | 1 |
| 41 | Weighted Random Selection / Lottery System | LC 528 | 1 |
| 42 | Stone Game II — Variant with more complex rules | LC 1140 variant | 1 |
| 43 | Minimum Sliding Window Substring | LC 76 | 1 |
| 44 | LC 1094 — Car Pooling | LC 1094 | 1 |
| 45 | LC 983 — Minimum Cost for Tickets (variant with edge cases) | LC 983 | 1 |
| 47 | Remove K Digits | LC 402 | 1 |
| 48 | LC 1263 — Minimum Moves to Move a Box to Target | LC 1263 | 1 |
| 49 | LC 399 — Evaluate Division | LC 399 | 1 |
| 50 | Max Subarray Without Repeating Characters | LC 3 | 1 |
| 51 | Tree Eccentricity — Find node with minimum max-distance to all others (tree DP) | Custom (tree DP) | 1 |
| 52 | Original / custom problems (non-LC, interviewer-designed) | — | 2 |
| 39 | LC 560 — Subarray Sum Equals K (prefix sum) | LC 560 | 1 |

---


## Part 3: Other Technical Components

| # | Topic | Count |
|---|-------|-------|
| 1 | **Resume Technical Deep-Dive** — Why you chose specific tech stacks, architecture walkthrough, trade-offs, tools used, how you judged results | 5 |
| 2 | **Data Structure Knowledge Check** — Interviewer asks about data structures (heap definitions, etc.) related to the upcoming coding question | 3 |
| 3 | **Live GenAI Demo** — Share screen and show how you use AI to solve a coding problem | 1 |
| 4 | **System Architecture Whiteboard** — Present and defend your internship project architecture on a whiteboard | 1 |
| 5 | **OS / Low-Level Concepts** — Follow-ups going deep into stack overflow, iterative vs. recursive, OS fundamentals | 1 |
| 6 | **Database Design Discussion** — Document-based vs. relational DB trade-offs, implementation critique | 1 |

---

### Notes

- The most dominant coding themes are **graph traversal (Islands/BFS/DFS/Union Find)**, **Top K**, **Course Schedule**, and **LRU/LFU**. These should be top-priority prep topics.
- **Tree DP** is emerging as a theme — multiple custom problems involve profit maximization on trees, eccentricity, and LCA-based path calculations.
- OOD questions often expect candidates to discuss **multiple approaches** and compare trade-offs — not just implement one solution.
- Some interviews combine BQ + Coding + OOD in a single session; others separate them across two rounds.
- Follow-up questions (space/time optimization, streaming input, edge cases, iterative vs. recursive, OS-level depth) are very common.
- **Whiteboard coding** is used in on-site Seattle interviews — practice writing code by hand and explaining line by line.
- Several candidates reported **custom / non-LC problems** — don't rely solely on pattern matching; understand the underlying algorithms deeply.