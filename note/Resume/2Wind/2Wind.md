# Internship
## 2Wind - 1 & 2
2Wind	January 2026 - April 2026
Software Developer Intern	Boston, MA
•	Updated PostgreSQL schemas by separating player profiles from season stats, simplifying cross-season queries and reducing redundant ingestion.
•	Built Python ingestion and backfill pipelines to migrate 16K+ player profiles and 72K+ game records from legacy APIs into Supabase/PostgreSQL.
•	Redesigned primary keys and upsert logic to eliminate duplicate records from repeated ingestion and support idempotent reruns.
•	Developed FastAPI endpoints for an AI coaching assistant, enabling agent-driven Q&A over player/team data through structured Supabase queries.


### General Note with Details - IGNORE
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

### Project Introduction

**"Can you walk me through what the product was, what problem you were solving, and what your role and contributions were?"**

Covering the context (what 2Wind does, why this work was needed), your specific responsibilities, and the key outcomes.

---
Sure, I'd love to.
Our team was building a trading platform for college football players — like a stock market but for sports. 
Coaches and team staff could browse and buy players to customize their roster, and we would provide suggested prices evaluated based on real game performance.

When I joined, the team was transitioning to a new external data source due to commercial license issue. 
My role was to redesign the database, build the data pipeline, and develop backend API. I will describe in three points.

First, I restructured the database schema. 
The original design was fairly flat: player identity info like name and birthday was mixed with season-dependent data like position and jersey number. 
That meant cross-season queries had to deal with redundant data everywhere. 
My key decision was to separate static player attributes and season-dependent statistics into different tables, so fetching a player's career history became a simple join rather than complex filtering.

Second, I built a player identity matching pipeline with a three-tier fallback: first try exact source ID lookup, then URL-based matching, and lastly normalized name matching for unmapped players. 
If all three fail, I would create a new player rather than taking the risk of merging two different people — because duplicates can be cleaned up later, but a wrong merge corrupts data. 
And because the pipeline translates all external IDs into internal UUIDs through a mapping layer, if data sources are switched again, only this mapping layer changes. No need to touch either the frontend or the backend.

Third was the idempotency issue — making sure rerunning the ingestion pipeline and get the same result. 
The original unique constraint was based on player, team, season, category, and source. 
However, I noticed that this could be broken in two ways. 
If a player transfers across season, the team ID changes, so the upsert can't find the existing record and would inserts a duplicate instead of updating the existing one. 
And the pipeline stores both per-game stats and season-level aggregates, which can be distinguished by the game_id field, but the old constraint didn't include it and could cause those two types of records overwrite each other.
My fix was to replace team_ID with game_ID in the unique constraint. 
After that, the pipeline became fully idempotent — no duplicates, no data loss.

This experience gave me a much deeper understanding of data modeling trade-offs and building reliable pipelines. 

---

### Follow-ups
#### 1. Schema Design Trade-offs

*"You mentioned separating player identity from season stats. What were the trade-offs of that split? Did it make anything harder or slower compared to the original flat design?"*

---
Let me take the seperation of player identity from season statistics as an example.
For this split, the main cost is that the query would require a JOIN.

In the original flat design, if we need a player's full career history, it's a single-table query -- everything was right there.
After this seperation, if we want both identity and seasonal data, we need to join two tables first based on the player_id.
This is an extra look-up, and in scale, JOINS do have a cost.

But in practice, this trade-off was totally worth it.
The previous flat table had player's name and birthday repeated on every season row.
Let's say, if a player has three season records, his name was stored three times.
That's not just a waste of storage, it could easily cause inconsistency issue.
For example, to correct a player's name, we would need to update every season rows; if one got missed, the same player would show two different names.
Now with this split, only one row in the player table needs to be updated, and then we'are done.

Besides, cross-season queries became nice and clean.
Instead of careful filtering to avoid repeated-counting on the identity fields, using JOIN and get exact one identity row with all season stats attached.
The outcome is more predictable, which makes viewing a player's full career history easier.

To be honest, this split did make some features harder.
For the player note feature, where users could put customized note on each players, the query now needs to JOIN three tables.
And for the frontend, they had to make extra API calls.
I solved that by encapsulating the JOIN behind the backend API endpoint: so for the frontend, it's still one call, one response, and the table structure is completely hidden.

Overall, we were optimizing data integrity over raw query speed, because our player data directly drives the price valuations that are the main idea of this product. 
Getting the wrong data means wrong prices, which is far more costly to the business than saving a millisecond on reads.

---

#### 2. Architecture & Tech Stack Choices

*"Why PostgreSQL and Supabase specifically? Did you consider other databases or architectures, and what drove the final decision?"*

---

Well, to be frank, Supabase and PostgreSQL already existed when I joined, but I can talk about why it is a reasonable choice.

Essentially Supabase provides a Postgres instance.
They have built-in authentication, row-level security, and REST API-- all ready to go.
For a startup with a small team, it is ideal to rely on existing infrastructure rather than building from scratch.

PostgreSQL, as a relational database, was a nice fit here, because our data is highly structured -- players belongs to teams, teams have seasons, etc. 
We also relied on its specific features like the JSONB column -- store statistics data in a flexible manner, and `NULLS NOT DISTINCT` from PostgreSQL 15.
So NULL is treated as a value and we can have NULL == NULL.
This is really important for idempotency, because season aggregates have NULL in the game_id field, and we need the database to treat two NULLs as equal to prevent repeat ingestion.

For alternatives, I think the key is about query pattern.
We'd like to support flexible query lookup by the AI assistant, and relational database handle this part more naturally.
For DynamoDB, the advantage is low latency, but this NoSQL database needs to be designed based on predictable access pattern.
If we reach the stage of prioritizing read latency or we can predict a clear search pattern, it would be great to have DynamoDb then.

---

#### 3. The Matching Pipeline
"For your three-tier player matching — how did you handle the normalized name matching in practice? How did you deal with edge cases like common names, nicknames, or typos?"

#### 4. Failure Handling & Observability
"When this pipeline ran against 72K+ records, how did you know it was working correctly? What happened when something failed midway — did you have monitoring, logging, or retry mechanisms?"

#### 5. Idempotency at Scale
"You replaced team_ID with game_ID in the unique constraint. How did you validate that the new constraint actually covered all edge cases? Did you run any kind of migration or backfill to fix existing duplicates?"


**Follow-up 3 — The Matching Pipeline**

*"For your three-tier player matching — how did you handle the normalized name matching in practice? How did you deal with edge cases like common names, nicknames, or typos?"*

Name matching was the last tier, and it was designed in a conservative way because of edge cases.
Normalization itself was simple: lowercase, strip special characters, and compare.
The main idea is: I only use name matching when the player was not mapped, and the name was unique within the same team and season.

For edge cases, 

> But the critical constraint was that I only used name matching when the player was **not already mapped** for this data source **and** the name was **unique** within the same team and season. So if there were two "John Smith" entries on the same team roster, name matching would refuse to pick either one, and both would be created as new canonical players.
>
> This was a deliberate choice. The three tiers are ordered by confidence: tier one — exact source ID match — is essentially guaranteed correct, because it's the same external ID we've seen before. Tier two — the synthetic CFBD URL — is also very high confidence, because it's a URL we generated from a previous CFBD import. Tier three — name matching — is the riskiest, so I put the strictest guard rails on it.
>
> For the edge cases you mentioned: nicknames and typos would simply fail the name match and result in a new player being created. That's intentional. A false negative — creating a duplicate that you clean up later — is far less damaging than a false positive — merging two different players into one record. If you merge incorrectly, their stats get combined, and now your ML model is pricing a player based on someone else's performance. That corrupts downstream valuations, which is the core of our product.
>
> In practice, the numbers tell the story. For the 2025 season, only 46 players failed all three tiers and were created as new entries. For 2024, it was about 5,700, but that's expected because 2024 was the first CFBD import — most players had no prior CFBD mapping to match against. On subsequent reruns of the same season, tier one catches essentially everything because the mappings are already established.
>
> If I were to improve this further, I'd probably add a fuzzy matching tier — maybe Levenshtein distance or phonetic matching — but gate it behind a manual review queue rather than auto-merging. That way you get the candidate matches surfaced without the risk of silent corruption.

---

**Follow-up 4 — Failure Handling & Observability**

*"When this pipeline ran against 72K+ records, how did you know it was working correctly? What happened when something failed midway — did you have monitoring, logging, or retry mechanisms?"*

> The primary mechanism was the dry-run / apply pattern. Every ingestion script had a `--dry-run` flag that would fetch the data from CFBD, run all the transformations, and print a summary of what it *would* do — how many inserts, updates, and skips — without writing anything to the database. I'd review those numbers first to check if they made sense. For example, if a dry run said it was about to create 15,000 new players for 2025 but I knew most of them should already exist, something was wrong — and that's actually exactly what happened early on, when a pagination bug only loaded 1,000 existing players into the lookup map, making the script think everyone else was new.
>
> For actual runs, I used a graduated rollout approach. The scripts support a `--team` flag, so I'd run against a single team first — like Florida or Air Force — verify the output manually, and only then run the full apply. There was also a `--max-new-players` flag that would halt the script if the number of new player inserts exceeded a threshold. This was a safety valve: if the identity matching was misbehaving, I'd rather stop at 200 new players than accidentally create 10,000 duplicates.
>
> When failures did happen midway — and they did — the idempotent design was what saved us. Because every write is an upsert against a natural-key constraint, a partial run doesn't leave the database in a corrupted state. It just leaves it incomplete. I could fix the bug, rerun the script, and the already-inserted rows would be matched and updated rather than duplicated. There was one specific case where the roster ingestion failed halfway through because of a unique constraint violation on `player_source_ids` — multiple CFBD keys were trying to map to the same canonical player. That left some players inserted but their mappings incomplete. After I fixed the mapping logic, I reran the same script and it completed cleanly because the idempotent upserts handled the partial state.
>
> For cleanup operations specifically — like removing legacy roster duplicates — I always created backup tables before deleting anything. The script would copy the target rows into a timestamped backup table, then perform the deletes. So if anything went wrong, we could restore from the backup.
>
> Post-run, I verified with SQL count queries: total rows per table, rows per season, null counts on key fields. Those numbers are all documented in the run logs. For example, after the 2024 roster ingestion, I checked that `player_source_ids` for CFBD had 21,366 rows, `roster_memberships` had 16,221 rows for 2024, and so on.
>
> What I didn't have was formal monitoring — no Datadog dashboards, no automated alerts. For a one-time migration at this scale, the manual verification approach was sufficient. But if this were a production pipeline running on a schedule, I'd add structured logging, row-count assertions that fail the job if counts deviate beyond a threshold, and alerting on ingestion failures.

---

**Follow-up 5 — Idempotency at Scale**

*"You replaced team_ID with game_ID in the unique constraint. How did you validate that the new constraint actually covered all edge cases? Did you run any kind of migration or backfill to fix existing duplicates?"*

> Validation happened at multiple levels.
>
> First, the migration itself was designed to be defensive. Before dropping the old constraint or creating the new one, the Alembic script checks whether the constraint actually exists. Same with the `game_id` column — it checks before adding. This meant the migration was safe to run even if the database was in some partial state from a previous failed attempt. And it had a full downgrade path: if the new constraint caused problems in production, we could roll back to the original constraint and drop the `game_id` column.
>
> Second, before writing the migration, I analyzed the existing data to understand what would happen. The key question was: would the existing rows satisfy the new constraint? Since the old data didn't have `game_id` at all — that column didn't exist yet — the migration adds it as nullable, and all existing rows get `game_id = NULL`. The new constraint treats all those NULL rows as distinct by default in standard SQL, which would mean they couldn't conflict with each other. That's actually fine for the existing data because the old rows were season-level aggregates — there should only be one per player per category per source, which the old constraint already enforced.
>
> But going forward, new season aggregates would also have `game_id = NULL`, and I needed upserts to work on those. That's where `NULLS NOT DISTINCT` came in — it tells PostgreSQL to treat two NULL values as equal for the purpose of this constraint. So if you insert a season aggregate for a player that already exists, the NULL game IDs match, the conflict fires, and the row gets updated instead of duplicated.
>
> For the per-game records — the 72K game stats — those were all new data being ingested for the first time, so there were no pre-existing duplicates to clean up. The new constraint just prevented duplicates from being created on future reruns.
>
> I validated the whole thing end-to-end by running the stats ingestion pipeline twice with `--apply`: once to load the data initially, and again to confirm that a rerun produced zero new inserts — only updates to existing rows. The row counts before and after the second run were identical, which confirmed the upsert was matching correctly on the new constraint.
>
> There was one edge case I specifically tested: a player with season-level stats (game_id NULL) and per-game stats (game_id = "401234") in the same category. In the old constraint, the season aggregate could accidentally overwrite a game row or vice versa because there was no way to distinguish them. With the new constraint, they're two separate rows — the NULL and the actual game ID are different values — so they coexist correctly.
>
> If I'd found existing duplicates from the old constraint, my plan was to deduplicate before applying the new constraint — keep the most recently updated row and delete the rest. But in practice, the old constraint was strict enough that duplicates hadn't accumulated; the problem was more about rows overwriting each other than coexisting incorrectly.

---




PostgreSQL 15's `NULLS NOT DISTINCT` feature so that season aggregates with a null game ID could still participate in upsert operations correctly. 


•	Built Python ingestion and backfill pipelines to migrate 16K+ player profiles and 72K+ game records from legacy APIs into Supabase/PostgreSQL.
> **Second, I built the ingestion pipeline.** This was a set of Python scripts that pull data from CFBD and load it into our Supabase PostgreSQL database. The pipeline runs in a strict order — sources, then teams, then players and rosters, then stats — because each step depends on the previous one's foreign keys. The stats ingestion was the trickiest part: CFBD returns data per game per team, with one row per stat type per player. So a single player's rushing stats in one game come back as four separate API rows. My transform layer regroups those into one structured JSON object per player per game per category. In total, I migrated about 16,000 player profiles and 72,000 per-game stat records across the 2024 and 2025 seasons.
>

>
•	Developed FastAPI endpoints for an AI coaching assistant, enabling agent-driven Q&A over player/team data through structured Supabase queries.
> **Fourth, I built the FastAPI endpoints** that connect the frontend to an AI coaching assistant. I set up the app entry point with CORS configuration, Pydantic data models, and two chat routes — one for standard responses and one for Server-Sent Events streaming — wiring the Next.js frontend to OpenAI's API. My teammate then built the agent logic on top of those endpoints.