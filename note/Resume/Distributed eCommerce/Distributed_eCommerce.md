# Project
## Distributed eCommerce

Distributed eCommerce Platform | Java, Spring Boot, MySQL, Redis, Kafka, Nginx	January 2025 - May 2025
•	Built a distributed backend for login, ordering, flash-sale, and engagement flows using Redis, Kafka, and MySQL under high-concurrency traffic.
•	Centralized session storage in Redis and added SMS rate limiting and blacklisting to support stateless scaling and prevent verification abuse.
•	Prevented flash-sale overselling with Redis request gating, optimistic locking, and Kafka-based async order processing during traffic bursts.
•	Shifted order creation to async workers backed by Kafka to improve throughput and reduce database lock contention under peak load.
•	Built a Redis and Kafka pipeline for likes to buffer bursty writes, offload MySQL, and stabilize high-frequency engagement updates.



### 1. Flash-Sale Abuse Prevention → Adversarial Thinking at Scale

Your **Distributed eCommerce Platform** project is your single best parallel. You built defenses against a fundamentally adversarial problem: preventing overselling during flash sales where bad actors (or just overwhelming traffic) can exploit race conditions. Specifically, you used Redis request gating, optimistic locking, and Kafka-based async processing to handle traffic bursts — this is the same *pattern* as IVT defense: you need to make fast, high-volume decisions about which requests are legitimate and which should be blocked, all under extreme time pressure and with financial consequences for getting it wrong.

**How to say it:** *"In my flash-sale system, I had to gate requests in real time and decide which ones to let through under enormous concurrency pressure — and the cost of a false negative was real money lost to overselling. That's a miniature version of what Ad Traffic Quality does: making high-stakes filtering decisions at massive throughput where both letting bad traffic through and accidentally blocking good traffic have direct financial impact."*
大规模的闪售滥用预防→对抗性思维
你的分布式电子商务平台项目是你最棒的对应项目。你建立了针对一个根本对抗性问题的防御：防止在闪售期间被恶意分子（或仅仅是流量过多）利用竞赛条件的超卖。具体来说，你使用了Redis请求门控、乐观锁定和基于Kafka的异步处理来处理流量突发——这与IVT防御的模式相同：你需要在极其紧张的时间压力下快速、大量决策，决定哪些请求是合法的，哪些应被阻断，且错误的财务后果。
怎么说呢：“在我的闪售系统中，我必须实时门关请求，并在巨大的并发压力下决定哪些请求通过——而假阴性的成本就是因过度销售而损失的真钱。这就像广告流量质量的缩影：在高吞吐量下做出高风险过滤决策，让坏流量通过和意外阻断优质流量都会直接产生财务影响。”

### Project Introduction

**"Can you walk me through what the product was, what problem you were solving, and what your role and contributions were?"**
### Follow-ups
#### 1. Schema Design Trade-offs


Let me read through all the project files to get the full picture.I've read all three files. Let me break down your project in priority order — starting with what matters most for the "adversarial, high-stakes filtering under concurrency" narrative you're preparing.

---

## 1. The Flash-Sale Pipeline — Your Core Story

This is the heart of your project and the strongest parallel to ad traffic quality. The architecture follows a **layered filtering** philosophy: each layer reduces request volume so the database only sees a tiny fraction of original traffic.

The flow is: **sync inventory to Redis → Gateway filters illegal requests → distributed rate limiting → load balancing → Redis atomic stock decrement → MQ async order creation → MySQL final write**.

What makes this adversarial: you're not just handling load, you're actively deciding *who gets through*. The gateway blocks bots, duplicate IPs, and malformed requests. The rate limiter (token bucket or counter via Redis) rejects the vast majority — if you have 100 items and 1M requests, you kill ~99.99% before they touch business logic. Then Redis `DECR` acts as the final gatekeeper: single-threaded execution means requests queue up and get deterministic yes/no answers. If stock hits 0, everyone after is rejected. If it goes to -1, you know to reject and the math stays clean.

The key insight for your interview narrative: **a false negative (letting a bad request through) costs real money — overselling means you owe product you don't have.** A false positive (rejecting a legitimate buyer) loses a sale but doesn't create liability. This asymmetry mirrors ad fraud filtering exactly.

## 2. Three Order Types — Escalating Defenses

You designed three distinct ordering flows matched to threat level:

**Normal orders** use optimistic locking only — the SQL `WHERE stock >= buyNumber` acts as a version check without an explicit version column. This is cheap and works because normal products rarely face contention. You made a smart optimization here: using `stock >= buyNumber` instead of `stock = queriedValue` avoids the cascade retry problem where N concurrent requests cause O(N²) database hits.

**Limited-purchase orders** add a Redis distributed lock keyed on `userId + couponId`. The reason: optimistic locking alone can't enforce per-user purchase limits in a distributed environment. Two requests from the same user hitting different servers would both pass the "have you bought this before?" check because the order hasn't been written yet. The lock serializes per-user-per-item decisions. You implemented this with `SETNX` + TTL for deadlock prevention, and Lua scripts for atomic lock release (check-then-delete).

**Flash-sale orders** go full async: Redis pre-checks eligibility and decrements stock, then the order payload goes into Kafka. The user gets "processing" immediately. Kafka consumers write to MySQL at their own pace — this is your **peak shaving** mechanism.

## 3. The Likes System — Your High-Throughput Read/Write Design

This shows architectural depth beyond the flash sale. You built a three-layer storage system (Caffeine local cache → Redis → MySQL) with a three-layer service system (service layer → async task layer → data layer).

The interesting design decisions: you use a Bloom filter to short-circuit "has this user liked this article?" queries — since most articles a user sees are new (recommendation algorithm), most like-status checks would be cache misses hitting the DB. The Bloom filter catches the majority of these "definitely not liked" cases. You also use Redis ZSets for like lists with score = timestamp, capped at 200 entries with trimming.

Write path: user likes → Kafka → consumer writes to `like_behavior` table → periodically aggregates counts into `article_count` and `user_count` tables. This batched count aggregation (e.g., every 5 seconds) massively reduces DB write pressure compared to incrementing on every like.

## 4. Failure Recovery — What Differentiates This From a Tutorial Project

You thought through what happens when things break:

- **Kafka consumer fails to write order to MySQL**: send to a dead-letter topic, a separate consumer runs a Lua script to atomically roll back Redis state (restore stock, remove order record, undo purchase limit).
- **Redis goes down mid-flash-sale**: drain remaining Kafka messages first (they represent committed-but-unwritten orders), then fall back to MySQL-direct with rate limiting enabled — degraded but consistent.
- **Kafka goes down**: orders already in Redis are preserved; write those to MySQL first, then accept new requests directly against the DB with circuit breakers.

The common thread: **MySQL is always the source of truth**, and every failure mode has a path back to consistency.

## 5. Login & Session — Supporting Infrastructure

Redis-based token sessions with dual interceptors (one for all paths to refresh TTL, one for auth-required paths to enforce login). Phone number + IP blacklisting with escalating penalties for SMS abuse. This is straightforward but shows you understand the full request lifecycle from authentication through to order completion.

---

**For your interview**: lead with the flash-sale pipeline (#1), pivot to the three-tier ordering logic (#2) to show you match defenses to threat levels, then mention the failure recovery (#4) to demonstrate you think about adversarial edge cases — not just the happy path. The likes system (#3) is your "I can also design read-heavy systems" card if they ask about breadth.

Want me to dive deeper into any specific area, or help you prepare specific talking points for the ad traffic quality angle?
1. 闪售流程——你的核心故事
这是你项目的核心，也是与广告流量质量最强的对应点。该架构遵循分层过滤理念：每一层都会减少请求量，因此数据库只能看到原始流量的极小部分。
流程是：同步库存到 Redis →Gateway 过滤非法请求→分布式限速→负载均衡→ Redis 原子库存减少→MQ 异步顺序创建→ MySQL 最终写入。
这对抗性之处在于：你不仅要承担负担，还要主动决定谁能通过。网关会阻止机器人、重复IP和错误的请求。速率限制器（通过Redis的token桶或计数器）会拒绝绝大多数——如果你有100件商品和100万个请求，你会在它们接触业务逻辑前杀掉~99.99%。然后 Redis 作为最终的守门人：单线程执行意味着请求排队并获得确定性的是非答案。如果库存为0，之后的所有员工都会被拒绝。如果降到-1，你就知道要拒绝，数学保持干净。DECR
你面试叙事的关键见解是：假阴性（让一个糟糕的请求通过）会花费真金白银——过度推销意味着你欠下自己没有的产品。误判（拒绝合法买家）会失去销售，但不会产生责任。这种不对称性与广告欺诈过滤完全相似。
2. 三种命令类型——逐步升级的防御
你设计了三种根据威胁级别匹配的不同排序流程：
普通订单仅使用乐观锁定——SQL 作为版本检查，没有明确的版本列。这种做法便宜且有效，因为普通产品很少会遇到争议。你做了一个聪明的优化：用 代替 避免了级联重试问题，即 N 个并发请求会导致 O（N²） 个数据库命中。WHERE stock >= buyNumberstock >= buyNumberstock = queriedValue
限量采购订单添加一个 Redis分布式锁，锁定于 。原因在于：仅靠乐观锁定无法在分布式环境中强制执行每个用户的购买限制。同一个用户的两个请求同时访问不同的服务器，都会通过“你以前买过吗？”的检查，因为订单还没写出来。锁对每个用户、每个物品的决策进行序列化。你用 + TTL 来防止死锁，用 Lua 脚本实现原子锁释放（检查后删除）。userId + couponIdSETNX
闪购订单完全异步：Redis预先检查资格并减少库存，然后订单有效载荷进入Kafka。用户能立即获得“处理”。Kafka的消费者以自己的节奏写入MySQL——这就是你的峰值削减机制。
3. 点赞系统——你的高通量读写设计
这显示了建筑深度超越了闪售。你构建了一个三层存储系统（Caffeine、本地缓存→Redis → MySQL），以及三层服务系统（服务层→异步任务层→数据层）。
有趣的设计决策是：你用布隆过滤器来短路“这个用户是否喜欢这篇文章？”的查询——因为用户看到的大多数文章都是新文章（推荐算法），大多数点赞状态检查会是缓存未中进入数据库。Bloom过滤器能捕捉大多数“绝对不受欢迎”的案例。你也可以用 Redis ZSets 来创建 score = 时间戳的点赞列表，并且通过修剪限制最多 200 条条目。
写入路径：用户喜欢→ Kafka→消费者写入表→定期汇总计数和表。这种批量计数聚合（例如每5秒）相比每次点赞递增，大大降低了数据库的写入压力。like_behaviorarticle_countuser_count
4. 故障恢复——它与教程项目的区别
你想过东西坏了会发生什么：

Kafka 消费者未能将订单写入 MySQL：发送到死符主题时，另一消费者运行 Lua 脚本原子回滚 Redis 状态（恢复库存、删除订单记录、撤销购买限制）。
Redis在闪售中期宕机：先排空剩余的Kafka消息（代表已承诺但未书写的订单），然后回退到MySQL-direct并启用速率限制——虽然降级但稳定。
卡夫卡倒下：雷迪斯已有的命令得以保留;先把这些写入 MySQL，然后直接用断路器对数据库接受新请求。

共同点是：MySQL始终是真相的源头，每种失败模式都有一条回归一致性的路径。
5. 登录与会话 — 支持基础设施
基于Redis的令牌会话，带有双拦截器（一个用于所有路径刷新TTL，一个用于强制登录的授权路径）。电话号码+IP被列入黑名单，短信滥用将面临逐步加重的处罚。这很简单，但说明你了解从认证到订单完成的完整请求生命周期。

面试时：先用闪售流程（#1），转向三层排序逻辑（#2），展示你将防御与威胁水平匹配，然后提及故障恢复（#4），表明你考虑的是对抗性边缘情况——而不仅仅是“快乐路径”。点赞系统（#3）是你“我也能设计大量阅读系统”的卡片，如果他们问广度。
想让我深入探讨某个特定领域，或者帮你准备广告流量质量方面的具体说话点吗？