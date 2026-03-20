As a professional SDE career coach, help summarize my work experience to put on the resume, which will be used for Google. My main responsibility in this experience (title: software developer intern, 01-03/2026, full-time) is to design baackend, reconstruct database schema, injest data from external API, data processing, and help implement a chatbot.

Now let's start collect information: you should always pause and ask me to clarify any uncertainty before generating internship description.

# Second Wind AI / college football player trading platform

## Overview
**Second Wind AI** is building a **college American football player trading platform** — essentially a marketplace where users on campus can "trade" college football players, similar in concept to fantasy sports or sports trading card platforms but focused specifically on college (NCAA) football.

The core idea is that each player has a **suggested price/value** determined by an ML model trained on the player's real performance statistics (passing yards, rushing stats, usage rates, etc.) pulled from the CollegeFootballData.com API. Users would buy and sell players based on these data-driven valuations.

The tech stack is Python/FastAPI backend, Supabase (PostgreSQL) database, and Next.js frontend. 

## Databse

**1. Switched Data Source from SportsReference to CFBD API**
- **Why:** The tech leader determined all existing data (Tim's SportsReference scrape, `source_id=1`) was unusable for the product. The CollegeFootballData.com API provides richer, more structured data with game-level granularity.
- **What was done:** Registered CFBD as `source_id=2` in the `sources` table via `ingest_cfbd_sources.py`. The old SportsReference rows (`source_id=1`) remain in the DB but are effectively deprecated.
- **Impact:** All downstream queries should filter by `source_id=2` to get clean CFBD data. The multi-source design means the old data isn't destroyed — it's just separated.

**2. Redesigned the `teams` Table + Created `team_seasons`**
- **Why:** The original schema stored season-varying attributes (conference, colors) directly on `teams`, which breaks when a team changes conference between years. Teams themselves are immutable entities.
- **What was done:** Yuan created the `team_seasons` table (keyed on `team_id + season_year`) to hold conference, division, classification, color, and alternate_color. The `teams` table was slimmed to just `school_slug` and `display_name`. She also populated `team_source_ids` to map CFBD's numeric team IDs to internal UUIDs. 140 FBS teams were ingested.
- **Impact:** Clean separation of static team identity from dynamic per-season metadata. Future conference realignment or color changes are handled without duplicating team records.

**3. Expanded the `players` Table Schema**
- **Why:** The original `players` table only had `full_name` and `player_url` (SportsReference-specific). CFBD provides richer biographical data needed for the trading platform's player profiles.
- **What was done:** Yuan's migration (`b9a5d7cf1e42`) added `first_name`, `last_name`, `display_name`, `home_city`, `home_state`, `home_country` columns. Made `player_url` nullable (CFBD players don't have SportsReference URLs). `player_source_ids` got `source_player_url` and `updated_at` columns. ~21,366 players were ingested across 2024–2025 seasons.
- **Impact:** The frontend and ML model now have structured name fields and hometown data for player cards/profiles, rather than parsing a single `full_name` string.

**4. Enriched `roster_memberships` with Physical/Roster Attributes**
- **Why:** The original roster table only had position and class_year. The trading platform needs physical measurements and jersey numbers for player evaluation and display.
- **What was done:** Added `height_inches`, `weight_lbs`, `jersey_number`, `position_raw`, `class_year_numeric`, `recruit_ids_jsonb`, and `raw_cfbd_payload` columns. Yuan's `ingest_cfbd_roster.py` populated these from CFBD's `/roster` endpoint. Legacy backup tables were created before the migration (`roster_memberships_legacy_backup_*`).
- **Impact:** The ML model has physical attributes as features. The `raw_cfbd_payload` column preserves the full API response for future re-processing without re-fetching.

**5. Resolved Legacy/CFBD Player Merge Conflict**
- **Why:** Jack discovered 15,190 players (Tim's old upload) had NULL values for all new CFBD columns. Yuan's initial script was too conservative and didn't overwrite existing rows.
- **What was done:** Yuan re-ran a backfill prioritizing CFBD data. Final state: 2024 is fully CFBD (16,221 players), 2025 has 15,601 CFBD + 1,301 unmatched legacy rows. She recommended filtering by `source_id=2` or `raw_cfbd_payload IS NOT NULL`.
- **Impact:** Clean data for the 97%+ of players that matched. The 1,301 legacy-only rows are harmless and filterable.

**6. Added `game_id` to `player_stats` + Rebuilt Unique Constraints**
- **Why:** The original `player_stats` had no way to distinguish per-game stats from season aggregates. The trading platform needs game-level granularity for the ML model's performance evaluation, and also needs to derive "games played" counts.
- **What was done:** Migration `c3f8a1d9e7b0` (chained after Yuan's) added the `game_id` column. Rebuilt both stats tables' unique constraints using PostgreSQL 15's `NULLS NOT DISTINCT` so that season-aggregate rows (`game_id=NULL`) and per-game rows can both be idempotently upserted. Also removed `team_id` from the player_stats constraint (players can transfer mid-season) and made `team_id` nullable.
- **Impact:** Enables `COUNT(DISTINCT game_id) WHERE game_id IS NOT NULL` to derive games played per player — no separate tracking needed. All upserts are idempotent, so re-running ingestion is safe.

**7. Ingested Player Statistics (4 Data Slices)**
- **Why:** Jack and the ML team were waiting on individual player statistics — this was the primary blocker for model training.
- **What was done:** `ingest_cfbd_stats.py` pulls from four CFBD endpoints:
  - **Game-level stats** (`/games/players`) — 72,193 rows upserted (138K fetched, deduplicated because both teams in an FBS matchup return the same game). 140 API calls, one per team.
  - **Season aggregates** (`/stats/player/season`) — 15,967 rows. 1 API call.
  - **Player usage** (`/player/usage`) — 3,048 rows. 1 API call.
  - **Team season stats** (`/stats/season`) — 8,568 rows. 1 API call.
  - Fake athlete entries (negative CFBD IDs like `-6165`) were filtered out (1,493 skipped).
- **Impact:** ~100K stat rows now available. Stats are stored as JSONB objects per player×category (e.g., one row with `stats = {"CAR": "120", "YDS": "546", "TD": "4"}`), making them flexible for the ML team to query without schema changes.

**8. Updated `models.py` (SQLAlchemy ORM)**
- **Why:** The ORM models were out of sync with the actual DB schema after migrations — `PlayerStats` was missing `game_id`, and both stats models had old constraint names.
- **What was done:** Updated `PlayerStats` to include `game_id`, changed `team_id` to nullable, renamed constraints to `uq_player_stats_natural_key` and `uq_team_stats_natural_key`. Caught and prevented a `back_populates` bug that would have crashed FastAPI at startup.
- **Impact:** API routes and any future SQLAlchemy-based queries now match the real schema. Prevents runtime errors.

**9. Established Ingestion Logging Convention**
- **Why:** Yuan requested that all ingestion work be documented in `server/logs/` so AI coding agents (Cursor, Claude Code, etc.) have context on what data exists and how it got there.
- **What was done:** Created `stats_ingestion_run_log.md` documenting the migration, all four data slices, row counts, design decisions (fake athlete filtering, JSONB grouping, team resolution via `source_name_raw`), and usage examples.
- **Impact:** Future developers or agents can read the log to understand what's in the database without reverse-engineering the scripts.

**10. Confirmed Production Environment Alignment**
- **Why:** Initial stats ingestion attempt landed in a local Supabase instead of production. Yuan noticed the data was missing and shared production credentials.
- **What was done:** Re-ran `ingest_cfbd_stats.py` against the shared production Supabase instance. Verified rows landed with spot-check queries.
- **Impact:** All team members (Jack, Yuan, the ML team) are now working against the same dataset. Also flagged that credentials were posted in a Slack channel — a security concern worth addressing.

## Data Procesing

**1. 基于 Airflow/Prefect 的定时 ETL 调度**

- **思路：** 把现有的四个 `ingest_cfbd_*.py` 脚本编排成一个 DAG（有向无环图），按依赖顺序执行：sources → teams → roster → stats。用 Airflow 或 Prefect 设置定时任务（比如赛季中每周一凌晨跑一次），自动拉取最新一周的比赛数据。
- **为什么适合这个项目：** 现在所有脚本已经是幂等设计（upsert），天然支持重复执行。主要工作量在于把"手动跑脚本"变成"自动调度+失败重试+Slack 告警"。
- **需要考虑的点：** CFBD 免费 API 限额 1000 次/月，调度频率要控制；赛季外（2–8月）可以降频或暂停。

**2. 增量同步 + CDC（变更数据捕获）**

- **思路：** 目前的脚本是全量拉取（比如一次拉 140 支球队的所有比赛），效率低且浪费 API 调用。可以改为增量模式：记录上次同步的最大 `game_id` 或日期，每次只拉新增的比赛和统计。Supabase 本身支持 Realtime（基于 PostgreSQL 的 logical replication），可以在数据写入后自动触发下游通知。
- **为什么适合这个项目：** 赛季中每周只有十几场新比赛，全量拉取 140 次 API 调用太浪费。增量同步可以把每次调用量从 ~140 降到 ~15-20。
- **需要考虑的点：** CFBD 的 `/games/players` 接口支持按 `week` 参数过滤，天然适合增量拉取。需要在数据库里加一张 `sync_state` 表记录每个数据切片的最后同步点。

**3. 数据质量监控 + 自动验证**

- **思路：** 目前数据质量问题靠人发现（比如 Jack 手动查出 15,190 条 NULL 记录）。可以在 ETL 流程的末尾加一组自动检查：行数是否在合理范围、NULL 比例是否异常、新赛季的球队数是否 ≈ 140、每支球队是否都有比赛数据等。检查失败时自动发 Slack 告警并阻断后续步骤。
- **为什么适合这个项目：** 团队是实习生为主，人员会轮换，不能依赖个人经验来发现数据问题。自动化验证是防止"脏数据进模型"的最低成本方案。
- **需要考虑的点：** 可以用 Great Expectations 或者简单的 SQL 断言脚本。初期不需要重工具，几十行 Python 就够。

4. Implementation

**选调度框架：Prefect 优于 Airflow**

For this project, Prefect is the better fit over Airflow. The team is small and intern-heavy, so the operational overhead of hosting an Airflow webserver + scheduler + metadata DB is hard to justify. Prefect can run as a single Python process, the existing scripts can be wrapped as `@task` functions with minimal refactoring, and Prefect Cloud's free tier gives you a dashboard and Slack notifications out of the box. The scripts already follow a clean pattern (CLI args, dry-run/apply, idempotent upserts), so wrapping them is mostly plumbing.

**整体架构**

The pipeline would be a single Prefect flow with four phases that run sequentially:

Phase 1 is **sync state check** — read a new `sync_state` table to determine what's already been ingested (last synced week, last synced season). Phase 2 is **incremental extraction** — only fetch what's new from CFBD. Phase 3 is **upsert into Supabase** — the existing script logic, unchanged. Phase 4 is **data quality validation** — run checks on what was just written, alert on failures.

**增量同步的具体做法**

The key insight is that CFBD's game stats endpoint supports a `week` parameter. So instead of fetching all 140 teams × all games every run, the sync logic becomes: look up the current NCAA football week (CFBD has a `/calendar` endpoint for this), compare it to `sync_state.last_synced_week`, and only fetch weeks that haven't been synced yet. For season-aggregate and usage endpoints, these are cheap (1 API call each) and can be re-fetched in full each run since they're overwritten by the upsert anyway.

The `sync_state` table would be simple — something like `(slice_name TEXT PRIMARY KEY, season_year INT, last_synced_week INT, last_run_at TIMESTAMPTZ, status TEXT)`. Each task updates its row after successful completion. If a run fails mid-way, the next run picks up from the last successful checkpoint.

This cuts API usage from ~140 calls per full run to roughly 15–20 calls for a weekly incremental sync, well within CFBD's 1,000/month free tier even with daily runs during the season.

**数据质量检查的实现**

Rather than introducing Great Expectations (overkill for this stage), I'd write a simple Python module — call it `validate_ingestion.py` — that runs SQL assertions against the data that was just ingested. The checks would cover things like: did we get a non-zero number of new rows for the target week? Is the NULL rate for key columns (player_id, category, stats) still at 0%? Is the total team count still around 140? Are there any orphaned player_ids that don't exist in the players table? Does every team with games this week have corresponding stat rows?

Each check returns pass/fail plus a diagnostic message. The Prefect flow runs validation as the final task — if any critical check fails, it marks the flow run as failed and sends a Slack webhook notification with the specific check that broke. Non-critical warnings (like a slightly lower row count than last week) get logged but don't block.

**赛季内 vs 赛季外的调度策略**

During the season (roughly weeks 1–15, September through early January), the flow runs weekly on Monday or Tuesday after game results are finalized. During the offseason, it switches to a much lower frequency — maybe monthly — primarily to pick up roster changes, transfers, and recruiting data that CFBD updates. The Prefect schedule can handle this with two deployment configurations, or a single flow that checks the current date and skips game-stats fetching if it's offseason.

**对现有代码的改动量**

The good news is that the existing scripts barely need to change. The main work is: creating a thin Prefect wrapper that imports the existing functions rather than calling them via CLI, adding the `sync_state` table (one small Alembic migration), adding a `--week` parameter to the game-stats slice of `ingest_cfbd_stats.py` so it can fetch a single week instead of all weeks, and writing the validation module. The core transform and upsert logic stays exactly as-is. I'd estimate this is roughly 2–3 days of work for someone familiar with the codebase.

## Chatbot

This feature has been implemented, which can refer to the uploaded word file.

## Clarification

1. **What did you personally implement vs. what teammates designed or completed?**
   I did: DB schema redesign, CFBD ingestion scripts, production data backfill / migration
   I collaborated with Jack to: Prefect incremental ETL design, and data validation / monitoring
   I helped implement with Bhavana: chatbot backend / tool integration

2. **Which database changes were actually your work?**
   I modify tables `team_seasons`, `player_source_ids`, `player_stats`, `roster_memberships`, redesign unique constraints / idempotent upserts
   Bhavana and I together: write Alembic migrations, update SQLAlchemy ORM models

3. **Which ingestion/data pipeline code did you write yourself?**
   I directly build: `ingest_cfbd_sources.py`, `ingest_cfbd_roster.py`, `ingest_cfbd_stats.py`, validation scripts
   I participated in: scheduler / Prefect flow

4. **Was the ETL automation actually implemented, or only designed?**
   partially implemented it

5. **What was your concrete contribution to the chatbot?**
   I worked on: backend API endpoints for the agent, tool wrappers for roster/stats/depth chart queries, prompt / workflow design, approval-state handling, Supabase integration,

6. **Do you have measurable outcomes tied to your work?**
   Not yet, but you can tell me which part to measure and I can go calculate now.

7. **What should the internship title/company/date line be exactly?**

   * **Software Developer Intern**
   * **Second Wind AI (current name) / Second Wind Pro (previous name)**
   * **Jan 2026 – Mar 2026, full-time**

8. **What angle do you want for Google?**
   I can optimize the bullets towards the angle of **backend + data platform with light AI support**.

## More Clarifications
1. total: 7 seasons for 2020-2025, 140 teams, 16492 players, 72190 game-level stat rows. 2. I didn't led anyone, better to soft to redesigned... 3. B. Partially implemented and tested, you shouldn't talk about if it is deployed or fully functioning 4. I collaborated with Bhavana, while I worked more for the backend support 5. Don't think about title/company, it doesn't matter here. 6. mostly A: Backend + data platform + data processing 7. 不写 deploy / production rollout，但会写 merged, supported, partially implemented/tested 这类更稳妥的词