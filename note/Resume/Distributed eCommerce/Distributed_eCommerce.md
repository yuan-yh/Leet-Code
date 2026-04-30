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