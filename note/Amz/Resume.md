# Internship
## 2Wind - 1 & 2
2Wind	January 2026 - April 2026
Software Developer Intern	Boston, MA
•	Updated PostgreSQL schemas by separating player profiles from season stats, simplifying cross-season queries and reducing redundant ingestion.
•	Built Python ingestion and backfill pipelines to migrate 16K+ player profiles and 72K+ game records from legacy APIs into Supabase/PostgreSQL.
•	Redesigned primary keys and upsert logic to eliminate duplicate records from repeated ingestion and support idempotent reruns.
•	Developed FastAPI endpoints for an AI coaching assistant, enabling agent-driven Q&A over player/team data through structured Supabase queries.


---

**Project Context:** Second Wind AI — a college football player trading platform where player valuations are ML-driven based on real NCAA stats. I was the sole backend/data engineer (one other person handled LLM logic, others on frontend and ML model training for player evaluations based on player statistics data).

**Schema Design:**

- **Before I joined:** A basic schema existed, populated from Sports Reference (source_id=1). It had a flatter structure — player profile data and season-varying data weren't cleanly separated. The company decided to change to CFBD for the business-use permission.
- **What I did:** Extended and restructured the schema for CFBD (source_id=2). The core principle: **static lifetime attributes** (name, birthday, photo_url) → `players` table; **season-varying attributes** (position, class year, salary, jersey number, recruiting stars) → `roster_memberships` table. This separation meant cross-season queries (e.g., "show me this player's career trajectory") became simple joins rather than requiring denormalization or complex filtering.
players JOIN roster_memberships ON player_id

强调的对比是：如果没有做这个分离（比如把所有数据都塞在一张大表里），你要么需要反范式化（denormalization）——同一个球员的名字、生日在每个赛季的行里重复存储；要么需要复杂的过滤逻辑来区分哪些字段是固定的、哪些是随赛季变化的。分离之后，一个简单的 JOIN 就自然地把"不变的身份信息"和"每赛季变化的数据"拼在一起了。

- **Multi-source identity resolution:** `player_source_ids` and `team_source_ids` tables map external IDs to internal canonical UUIDs. This decouples the internal data model from any single API provider — if you swap CFBD for another source tomorrow, only the mapping layer changes.

后端和前端只用内部 UUID，所以换数据源对它们没有影响。
Ingestion: 拿到新 API 的外部 ID 后，去 player_source_ids 表里查：这个外部 ID 有没有对应的内部 UUID？如果有，就复用；如果是新球员，就生成一个新的 UUID，然后在映射表里插入一条新记录。

如果没有这个映射层，外部 ID 会散落在各张表里，换数据源就意味着要全库替换 ID，风险大、改动多。这就是所谓的"解耦"——用一张中间映射表把外部世界的变化隔离在最外层。

- **Stats stored as JSONB with category discrimination:** One `player_stats` table handles game stats, season aggregates, usage, athletic testing, and scouting grades via a `category` column + JSONB `stats` field. Avoids table proliferation; same query patterns work across all stat types.
- **Additional tables I created:** `depth_chart` / `depth_chart_assignment` (coach-editable), `player_notes` (structured coach evaluations by category). Used Alembic for all migrations with proper up/down reversibility.

**Ingestion Pipeline:**

- **Ordered multi-step:** sources → teams → players/rosters → stats. Each step is a standalone Python script with `--dry-run`, `--apply`, `--team` (single-team safety run), `--max-new-players` flags.
- **The hard part with stats:** CFBD returns stats per game per team, one row per stat type per player. So a single player's rushing stats in one game come as 4 separate API rows (CAR, YDS, TD, Y/A). My transform functions invert this into one JSONB object per player × game × category. Also had to filter fake athlete entries (negative IDs like `"-6165"` for team aggregates).
- **Performance:** Bulk-loaded team and player lookup maps into memory dicts at startup, avoiding per-row DB queries during transformation.
如果不优化： 每处理一条记录，都要去数据库查一次"这个外部 ID 对应的内部 UUID 是什么"。72K 条记录就是 72K 次数据库查询，非常慢，因为每次查询都有网络往返的开销。
实际做法： 在脚本启动时，一次性把 player_source_ids 和 team_source_ids 两张映射表全部加载到内存里，变成 Python 的 dict.
之后处理每条记录时，直接在内存里 dict 查找，O(1) 时间复杂度，不需要访问数据库。72K 条记录可能从几分钟变成几秒钟。

- **Identity matching:** 3-tier fallback — (1) existing CFBD source mapping by `(source_id, source_key)`, (2) synthetic CFBD URL fallback, (3) unique normalized-name fallback only if not already mapped. Conservative approach: if all filters fail, create a new canonical player rather than risk a wrong merge.
- **Scale:** ~136 teams, ~16K player profiles (per season), ~72K per-game stat records, across 2024-2025 seasons.
- **Currently one-time scripts**, but designed for future automation — the `--year` flag, idempotent upserts, and dry-run mode all support scheduled reruns.

**Idempotency (the most technically interesting piece):**

- **Core mechanism:** Natural-key unique constraints + `INSERT ... ON CONFLICT DO UPDATE` (upsert via Supabase client).
Natural-key unique constraint（自然键唯一约束）： 在表上定义一组字段的组合必须唯一。比如"同一个球员 + 同一赛季 + 同一场比赛 + 同一统计类别 + 同一数据源"只能有一条记录。
INSERT ... ON CONFLICT DO UPDATE（upsert）： 插入数据时，如果违反了唯一约束（说明这条数据已经存在），就自动变成更新操作，而不是报错或插入重复行。

- **The problem I solved:** The old unique constraint on `player_stats` was `(player_id, team_id, season_year, category, source_id)`. This broke in two ways: (a) no `game_id`, so per-game rows couldn't be distinguished from season aggregates, and (b) `team_id` was in the constraint, which broke for mid-season transfers.
旧的唯一约束是 (player_id, team_id, season_year, category, source_id)，有两个缺陷：
缺陷 a：没有 game_id。 系统里有两种统计数据——单场比赛的和整赛季汇总的。没有 game_id 的话，数据库无法区分"Mahomes 第一场比赛的 passing 数据"和"Mahomes 整个赛季的 passing 汇总"，因为它们的 player_id、team_id、season_year、category、source_id 全部一样，会被当成同一条记录互相覆盖。
缺陷 b：team_id 在约束里。 如果一个球员赛季中途转队了，比如上半赛季在 A 队、下半赛季在 B 队，他的赛季汇总数据应该只有一条记录。但因为 team_id 在唯一约束里，A 队一条、B 队一条，变成了两条，语义上就错了。而且再次导入时，如果数据源只给你最终球队的汇总，upsert 会插入新行而不是更新旧行，因为 team_id 变了，匹配不上。
- **My fix:** New constraint `UNIQUE NULLS NOT DISTINCT (player_id, season_year, game_id, category, source_id)`. Removed `team_id`, added `game_id`. Used PostgreSQL 15's `NULLS NOT DISTINCT` so `game_id=NULL` (season aggregates) can participate in uniqueness checks and upsert correctly.
新的唯一约束改成了 (player_id, season_year, game_id, category, source_id)：
去掉了 team_id： 转队问题解决了。不管球员在哪个队，只要是同一个人 + 同一赛季 + 同一场比赛 + 同一类别，就认为是同一条记录。
加上了 game_id： 单场数据的 game_id 有具体值，赛季汇总的 game_id 是 NULL。这样两种数据就能区分开了。
但这引入了一个新问题： 在 SQL 标准里，NULL ≠ NULL。也就是说两条 game_id=NULL 的记录，数据库不认为它们在这个字段上冲突，upsert 就失效了——赛季汇总数据每跑一次就多一条。
解决办法： 用 PostgreSQL 15 的新特性 NULLS NOT DISTINCT，告诉数据库"在这个约束里，NULL 等于 NULL"。这样两条 game_id=NULL 的记录也会被视为冲突，upsert 就能正常工作了。

- **The migration itself** (the Alembic file you shared) is defensive — it checks if tables/columns/constraints exist before operating, making it safe to rerun. Proper downgrade path restores the original constraint and drops `game_id`.
问题是：如果脚本跑到一半失败了怎么办？或者有人手动改过数据库结构了呢？所以脚本在每一步操作之前都先检查当前状态.
这样不管数据库处于什么中间状态，脚本都能安全地跑到正确的终态，不会因为"列已存在"或"约束找不到"而崩溃。
另外还写了 downgrade 路径：如果新约束上线后出了问题，可以回滚——删掉新约束和 game_id 列，恢复旧的约束。这是 Alembic 的标准实践，每次 upgrade 对应一个 downgrade。

- **Sources table:** Hit a concrete bug — auto-increment wasn't configured, so explicit ID computation was needed.
- **Roster ingestion:** Hit a unique constraint violation on `player_source_ids` when multiple CFBD keys mapped to the same canonical player. Fixed by enforcing one-to-one source mapping order.

**FastAPI + LLM:**

- Built a FastAPI app entry point with CORS config, Pydantic request/response models, and two chat routes: one for normal responses, one for SSE streaming.
- This was the API layer connecting the Next.js frontend to OpenAI's API. I wrote the endpoint plumbing; the LLM agent logic (tool definitions, prompt engineering for querying Supabase) was handled by a teammate.

**Legacy Data Cleanup:**

- Ran backfill scripts to update 13,906 legacy (Sports Reference) player profiles with richer CFBD data.
- Ran multi-phase roster dedup: strict match cleanup (356 rows), then CFBD-priority same-name conflict resolution (73 rows), always creating backups before deletion.

---























## CLYNK - 1 & 2
Roux	September 2024 - December 2024
Software Developer Intern	Boston, MA
•	Built a billing platform with React, TypeScript, Node.js, and PostgreSQL to manage distributor-facing invoice creation, validation, and tracking.
•	Optimized React rendering and state updates in invoice dashboards, reducing page load time 20% and increasing user engagement by 15%.
•	Designed REST APIs for invoice submission, validation, and status updates, reducing processing time 25% and improving data consistency by 30%.
•	Optimized SQL queries and redesigned the invoice schema, cutting query latency 40% and reducing data redundancy 35% across 50,000+ products.
•	Added idempotency checks at the API and database layers to prevent duplicate invoice submissions and avoid inconsistent financial records.

Data for Social Good	September 2025 - December 2025
Software Developer Intern	Portland, ME
•	Architected and implemented a scalable full-stack billing management app using Vue, TypeScript and React Native; designed RESTful APIs and async job processing in Redis for invoice workflows with beverage distributors
•	Revamped invoice dashboards using Vue.js, achieving a 20% reduction in page load time by optimizing component rendering and state management, which enhanced user engagement by 15%
•	Optimized SQL queries and restructured the database schema for the invoice management system, reducing data redundancy by 35%, cutting query response time by 40% and boosting invoice retrieval efficiency across 50,000+ products
•	Safeguarded financial data integrity using idempotency keys at the API and database layers to prevent duplicate invoice submissions, async job queues to decouple heavy operations from the main request path

## cPort - 1
cPort Credit Union	July 2025 - December 2025
AI Developer Intern	Boston, MA
•	Built a real-time AI translation platform for Credit Union serving non-English speaking customers, integrating Next.js frontend and FastAPI backend with fine-tuned LLM via streaming APIs; drove 30% increase in immigrant customer retention
•	Fine-tuned multilingual translation models using LLaMA-Factory with LoRA on 5K+ domain-specific banking term samples; achieved 25% improvement in financial term accuracy evaluated on 500-sample held-out test set
•	Architected RAG-based system with vector embeddings for smooth and continuous financial and bank terms update
 
## Breast Cancer - 2
Rou Intelligence Lab	May 2025 - September 2025
AI Research & Developer Intern	Boston, MA
•	Designed an AI-assisted breast cancer screening platform for underserved clinics to identify high-risk cases faster and generate structured clinical reports for documentation.
•	Built a multi-agent workflow with FastAPI and LangGraph for VLM analysis, retrieval, and case routing in ultrasound review.
•	Developed a modular RAG pipeline over medical literature with Qdrant hybrid retrieval and reranking to provide clinical advice.

# PROJECTS
## 1 - Distributed eCommerce System | Java, Spring Boot, MySQL, Redis, Kafka, Nginx	August 2024 - December 2024
•	Built a distributed eCommerce backend for auth, ordering, flash-sale, and social engagement flows under high-concurrency traffic.
•	Centralized session storage in Redis and added SMS rate limiting / blacklisting to support stateless scaling and prevent verification abuse.
•	Prevented flash-sale overselling using Redis request gating, optimistic locking, and Kafka-based async order processing during traffic bursts.
•	Shifted order creation to async workers to increase throughput and reduce database lock contention during peak traffic.
•	Built a Redis + Kafka likes pipeline to absorb bursty writes, smooth downstream load, and stabilize high-frequency engagement updates.
 
## 1 - GeneWeaver Backend System | Python, PostgreSQL, SQ-Lite, REST API	January 2025 - June 2025
•	Developed REST API for Jackson Laboratory using Python & Flask in Scrum environments
•	Designed backend logics for gene-set upload with data insertion and retrieval with PostgreSQL and SQ-Lite; Integrated analytical tools in microservices and mitigated downtime during tool update by 18%
•	Optimize runtime performance on concurrent tasks using Async Python and recurrent analytical queries using Page Caching; Implemented secure data access point using HTTPS protocols & web authentication

## 1 - Microservice-based eCommerce Platform | React, Express, MongoDB, Node.js	January 2025 - May 2025
•	Built up a MERN stack-based eCommerce platform; Developed and maintained software features to enhance customer engagement through front-end UI components, REST API services, and data modeling 
•	Designed data model using MongoDB; integrated Mongoose for query searching performance enhancement and Redis for schema definition; Leveraged JWT for API authentication and Redux Toolkit for state management 
•	Applied Postman for integration testing and Stripe API for payment; Utilized Heroku for deployment & CI/CD pipeline for smooth deployment

## 2 - Relational Database Management System | C++, Storage Engine, Query Execution	January 2024 - June 2024
•	Implemented a thread-safe buffer pool manager in C++ to cache disk-backed database pages, manage replacement, and coordinate concurrent access.
•	Built a concurrent B+Tree index to enable indexed lookups, ordered scans, and page-based updates in a multi-threaded engine.
•	Developer relational operators for scan, join, aggregation, and index access to execute SQL query plans over indexed tables.

## 1 - Emotion-tracking Android Mobile App | Java, Android SDK, Firebase	May 2023 - December 2023
•	Developed a mobile app for effortless mood tracking and analysis with Java to manage mental health
•	Implemented real-time data synchronization across multiple devices and secure user management through Firebase Real-Time Database and Firebase Auth; Enhanced user engagement through timely and personalized notifications using Firebase Cloud Messaging 

