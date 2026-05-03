## Notes
- Common Follow-up: why, trade-offs, how you measured success, etc.
- Prepare **7+ stories** for: Fail/Mistake, Outside Responsibilities, Tight Deadline, Gen AI, Challenging Project, Conflict, and Deep Dive.


## Tier 1: Very High Frequency
### 1. Deep Dive
A time you had to deep dive into a problem or topic / find the root cause / analyze a bug + 追问拷打
建議有在準備的好好想一下，這題比較像你解決一個bug 或是 service 壞掉，你怎麼找到root cause
dive deep root cause wasn't obvious problem, but you found out -> follow-up: how do you find that out
follow up- dive deep：怎么弄优先级 如果你已经弄了12task 还剩34怎么办

The key is to show how do you find the root cause.

Situation:
During my previous internship, the team was building a trading platform for college football players where prices are driven by real game data. 
I was building an ingestion pipeline to ingest player's seasonal data into PostgreSQL. 
After running the pipeline for 2025 during development environment, I noticed some players have multiple season aggregates for the same year. 
The season aggregates are like year summary, which should only exist one per year. 
That means the pipeline wasn't idempotent even though it used upsert logic with a unique constraint.

Task:
Soon as I realized, I brought it up in the tech drop-in meeting to notify the team. 
My mentor confirmed this should be top priority, so I took full ownership of diagnosing and fixing the pipeline to preserve data integrity.

Action:
I started by running a GROUP BY query to find all players with more than one season aggregate for the same year. 
Then I pulled the full duplicated rows side by side, and noticed the duplicates had different team IDs — these were transfer players. 
Because team_id was part of the unique constraint, a mid-season transfer made the upsert treat it as a new record instead of an update. That was the first failure mode.

The second was that per-game stats and season aggregates were both in the same table, distinguished only by the game_id field. But game_id wasn't in the unique constraint, so a per-game row could silently overwrite a season aggregate. On top of that, I discovered a PostgreSQL-specific complication: season aggregates had NULL in game_id, and PostgreSQL treats NULL ≠ NULL by default — so two NULLs wouldn't trigger a conflict, and both would get inserted.
Once I had all three causes mapped out, I synced with my mentor. He pointed me to PostgreSQL 15's NULLS NOT DISTINCT feature for the NULL handling, and we discussed with the tech lead to confirm it was safe to modify the existing constraint. My fix was to replace team_id with game_id in the unique constraint, which cleanly separated per-game rows from aggregates and removed the dependency on a value that changes with transfers.

Result:
After the fix, the pipeline became fully idempotent — rerunning it produced no duplicates or data loss. 
This was critical for accurate price evaluations, which was the main idea of this product.

Learn:
From this experience, I learned that idempotency bugs often hide in the assumptions behind your unique constraints. 
Now when I design any upsert logic, I always ask myself: "which fields in this constraint could change over time?" and "are there NULLs that need special handling?" 
Also, my mentor's suggestion about NULLS NOT DISTINCT saved me hours of building a workaround — it reinforced that reaching out early is faster than working around a problem alone.


> Q1: "How did you actually find the root cause? Did you run SQL queries, look at logs, or what?"
Yes, it started with a simple count query. After running the pipeline twice, I ran something like SELECT player_id, season, COUNT(*) FROM stats GROUP BY player_id, season HAVING COUNT(*) > 1 to find duplicated rows. That gave me a list of players with duplicates. Then I pulled the full rows for a few of those players and compared them side by side — same player, same season, but different team IDs. That's when it clicked: these were transfer players. The team_id was part of the unique constraint, so when it changed, the upsert treated it as a new record.
For the second issue — per-game stats overwriting season aggregates — I found it by noticing that some season aggregate rows had suspiciously specific numbers that looked like single-game stats. I queried for rows where game_id was NULL (aggregates) and compared them against what the source API actually returned. The numbers didn't match. That told me the per-game row was overwriting the aggregate because the constraint couldn't distinguish them.
So it wasn't one big "aha" moment. It was querying for anomalies, comparing against the source of truth, and working backward from "what data is wrong" to "what assumption in the constraint allowed this."

问1：“你是怎么找到根本原因的？你有运行SQL查询、查看日志，还是别的什么？”
是的，这一切始于一个简单的计数查询。运行了两次管道后，我运行了类似寻找重复行的程序。那给了我一份有重复角色的球员名单。然后我拉出了其中几位球员的整行，并并排对比——同一个球员，同一赛季，但球队ID不同。那时他才恍然大悟：这些人是转会球员。team_id是独特限制的一部分，所以当它变更时，Upsert将其视为新纪录。SELECT player_id, season, COUNT(*) FROM stats GROUP BY player_id, season HAVING COUNT(*) > 1
关于第二个问题——每场比赛统计覆盖赛季总数据——我发现有些赛季总数据行的数字异常具体，看起来像单场比赛统计。我查询了哪些行game_id为NULL（聚合），并与源API实际返回的行进行了比较。数字不匹配。这告诉我，每场比赛的行覆盖了聚合，因为约束无法区分它们。
所以这并不是一个巨大的“啊哈”时刻。它在查询异常，与真实来源进行比较，并从“哪些数据错误”倒推到“约束中的假设允许了这一点”。

> Q2: "How did you prioritize? You mentioned two separate bugs in the constraint — did you fix them together or one at a time?"
I fixed them together, because they were both rooted in the same unique constraint. But I did prioritize which one to investigate first. The transfer-player duplication was more urgent because it produced visible duplicates — the record count was growing, and downstream price calculations could double-count a player's stats. The overwrite issue was sneakier because the record count looked correct; it was the values that were wrong. So I tackled the visible problem first to stop the bleeding, and the investigation naturally led me to the second issue.
If I had been in a situation where these were truly separate tasks and I could only finish one, I would fix the duplication issue first because it's the more damaging failure mode — wrong record count affects every query downstream. The overwrite issue is also bad, but it only affects players who have both per-game and aggregate data in the same season, which is a smaller blast radius.

问2：“你是如何优先排序的？你提到约束中有两个不同的bug——是一起修复的，还是一次修复一个？”
我把它们合并在一起，因为它们都根植于同一个独特的约束。但我确实优先考虑了先调查哪一个。转会球员的重复更为紧迫，因为它会产生明显的重复数据——记录数量不断增长，下游价格计算可能会重复计算球员的统计数据。覆盖问题更为隐蔽，因为记录计数看起来正确;是价值观错了。所以我先解决了明显的问题以止血，调查自然引出了第二个问题。
如果我遇到这些任务真的是独立的，只能完成一个，我会先解决重复问题，因为这是更严重的失败模式——错误的记录计数会影响下游的每一次查询。覆盖问题也很严重，但只影响那些在同一赛季同时拥有场均数据和总数据的球员，而这些数据的爆炸半径较小。

> Q3: "How did you verify your fix actually worked?"
I ran the pipeline twice on the same dataset and compared. First, I checked that the total row count was identical after both runs — no new rows created. Second, I spot-checked a few known transfer players to confirm their records were updated in place rather than duplicated. Third, I compared season aggregate values against what the source API returned to make sure per-game stats weren't overwriting them anymore. I also ran that same HAVING COUNT(*) > 1 query to confirm zero duplicates across the entire table.

问3：“你是怎么验证你的修复真的有效的？”
我在同一数据集上运行了两次管道并进行了对比。首先，我检查了两次运行后总行数是否相同——没有新行被创建。其次，我抽查了几名已知转会球员，确认他们的记录是现场更新的，而不是重复的。第三，我将赛季总值与源API返回的数据进行比较，以确保每场比赛的统计数据不再覆盖它们。我还运行了同样的查询，确认整个表没有重复。HAVING COUNT(*) > 1

> Q4: "What if the pipeline fails halfway through — say it ingests 5,000 out of 16,000 players and then crashes? What happens on rerun?"
That's exactly why idempotency mattered. Because the upsert logic now correctly identifies existing records, rerunning the pipeline after a partial failure just picks up where it left off. The 5,000 already-ingested records get matched by the unique constraint and updated (even if nothing changed), and the remaining 11,000 get inserted as new rows. There's no special recovery logic needed — you just rerun the whole thing.
I did add basic logging so we could see how many rows were inserted vs. updated on each run, which made it easy to confirm after a crash that the rerun actually processed everything.

问4：“如果流水线在中途失败——比如它吞噬了16,000名玩家中的5,000名玩家，然后崩溃？重播时会发生什么？”
这正是幂零性重要的原因。由于upsert逻辑现在能正确识别已有记录，部分失败后重新运行流水线会从中断处继续。已经导入的5,000条记录会被唯一约束匹配并更新（即使没有任何变化），剩下的11,000条则作为新行插入。不需要特殊的恢复逻辑——你只需重新运行整个过程。
我确实添加了基础日志，这样我们可以看到每次运行插入了多少行或更新了多少行，这让崩溃后更容易确认重播是否处理了所有内容。

> Q5: "Did you consider any alternative approaches to fixing the constraint?"
Yes. One option was to keep team_id in the constraint and add application-level logic to detect transfers — basically, before inserting, query whether this player already has a record for this season under a different team, and update that row instead. But that adds a round-trip per player and moves correctness logic into the application layer, where it's harder to enforce universally. If someone writes a new script that touches the same table, they'd need to replicate that logic.
The constraint-based approach is better because it's enforced at the database level — no matter how data enters the table, the rule applies. That felt more aligned with "defend data integrity at the lowest possible layer."

问5：“你考虑过其他修复约束的方法吗？”
是的。一种选择是保留team_id在约束中，并添加应用级逻辑来检测转会——基本上，在插入之前，先查询该球员是否已经拥有本赛季其他球队的记录，然后更新该行。但这增加了每位玩家的往返，并将正确性逻辑移入应用层，更难普遍执行。如果有人写了新的脚本，涉及同一个表，他们就需要复制那个逻辑。
基于约束的方法更好，因为它在数据库层面被强制执行——无论数据如何进入表，规则都适用。这更符合“在最低层保护数据完整性”的理念。

> Q6: "你怎么弄优先级？如果你已经弄了一半的 task 还剩一半怎么办？" (How do you prioritize? If you've done half your tasks and still have half left?)
My prioritization framework for this project was: data correctness first, then completeness, then convenience. Anything that could produce wrong data (like the constraint bug) got fixed before things that were merely incomplete (like missing players from the migration). And incomplete data got handled before nice-to-haves (like cleaner logging or better error messages).
If I had finished only half my tasks — say I'd fixed the schema and the idempotency issue but hadn't built the identity matching pipeline or the API endpoints — I would first communicate clearly to the team about where things stand and what's left. Then I'd document my progress so someone could pick it up: what's done, what the remaining tasks are, what decisions I already made and why. I'd also flag which remaining tasks carry the most risk if delayed — for example, the identity matching pipeline blocks all future ingestion, so that's higher priority than API endpoints which are only needed when the frontend is ready.
The worst thing you can do is quietly leave tasks unfinished without telling anyone. Even if the work isn't done, the team can plan around it if they know.

Q6：“你怎么弄优先级？如果你已经弄了一半的任务还剩一半怎么办？”（你如何优先排序？如果你已经完成了一半任务，还剩下一半？）
我为这个项目制定的优先级框架是：数据正确性优先，然后完整性，然后便利性。任何可能产生错误数据（比如约束漏洞）都会在一些不完整的问题（比如迁移过程中缺少玩家）之前就被修复了。而且不完整的数据在“可有可为”（比如更干净的日志记录或更好的错误信息）之前就被处理了。
如果我只完成了一半任务——比如我修复了模式和幂等性问题，但还没搭建身份匹配流水线或API端点——我会先明确告诉团队目前的状况和剩余内容。然后我会记录进度，让别人能接手：完成了什么，剩下的任务是什么，我已经做了哪些决定，为什么。我还会标记出哪些剩余任务如果延迟风险最大——例如，身份匹配流水线阻止所有未来的采集，这比只有前端准备好时才需要的API端点优先级更高。
最糟糕的做法就是悄悄地把任务放着不做，却不告诉任何人。即使工作还没完成，团队如果知道，也能围绕它进行规划。

### 2. Tight Deadline
2. **Tight Deadline** — How you handled a tight deadline or delivered under time pressure / 没有完成的情况 | 24 |
Follow-up: 花了多长时间交付 是否做出牺牲

Situation: During my startup internship, we needed to deliver a full-stack MVP for a sports player tax filing platform. The catch was we only had two weeks — the product had to go live before tax season started to gain confidence from both customers and partner banks.

Task: As a full-stack developer, I was responsible for building and shipping the working MVP within that two-week window.

Action: 
Unerstanding the urgency, I prioritize tasks effecitvely and broke down the project into smaller manageable components.
This allowed me to focus on the most cruicial functionalities and ensure their timely completion. 
I started by listing every feature the stakeholders had requested, then sat down with my manager to ruthlessly prioritize. 
We identified three core features that would make the product usable — user registration, document upload, and a basic tax summary dashboard — and explicitly deferred nice-to-haves like notifications and analytics. 
Next, I talked with my mentor and discovered we had reusable authentication and file-upload modules from a previous internal project, which saved roughly two days of work. 
I set up daily standups (even though the team was small) so blockers surfaced within hours instead of days. 
I also made an architectural tradeoff: instead of building a custom backend API for everything, I used Supabase for auth and storage so I could focus my time on the business logic and frontend. By day five I had a working version deployed, and we spent the last two days doing live testing with a pilot user.
Throughout the project, I maintained proactive communication with my team and manged to provide regular updates on the progress. This ensured that everyone was on the same page and allowed for timely feedback and adjustments when needed.
动作场面：我先列出了利益相关者要求的每一个功能，然后和经理坐下来严格优先排序。我们确定了三个核心功能，使产品可用——用户注册、文件上传和基础税务摘要仪表盘——并明确推迟了通知和分析等“可有”功能。接着，我和导师聊过，发现我们有之前内部项目的可复用认证和文件上传模块，节省了大约两天的工作时间。我安排了每日站立会议（尽管团队很小），所以阻碍者几小时内就能出现，而不是几天。我还做了一个架构上的权衡：没有为所有东西构建自定义后端 API，而是用 Firebase 来做认证和存储，这样我可以把时间集中在业务逻辑和前端上。到了第五天，我已经部署了一个可用的版本，最后两天我们用试点用户进行了实时测试。

Result: 
As a result, despite the tight deadline, our teams' efforts and effective coordination resulted in a sooth and efficient launch.

We launched on time before tax season. The pilot customer successfully uploaded their documents and the partner bank confirmed the integration worked. The on-time delivery helped the startup close its next round of user partnerships.
结果：我们在报税季前按时启动。试点客户成功上传了他们的文件，合作银行也确认了集成成功。准时交付帮助初创公司完成了下一轮用户合作。

Learn: I learned that tight deadlines are really prioritization problems in disguise. Saying "no" (or "not yet") to features early is what makes saying "yes" to the deadline possible. I also learned the value of seeking out existing resources before writing anything from scratch.
学习：我了解到，紧迫的截止日期其实是伪装成优先级问题的伪装。提前对专题说“不”（或“还没”），正是让对截止日期说“是”成为可能的关键。我也学会了在从零开始写任何东西之前，先寻找现有资源的重要性。

Miss the DDL Case:
“错过截止日期”报道——发布后税务计算功能
情况：在我们按时发布了报税平台的MVP后，下一个冲刺目标是在两周内添加自动化税务计算引擎。我的经理把这个时间表交给了合作银行，因为他们想向合规团队演示完整的工作流程。
任务：我拥有计算模块——负责处理上传的文件、提取收入字段，并根据玩家所在州的居住地计算预估税负。
动作场面：我低估了它的复杂性。每个州对运动员收入分配有不同的规定，我原以为网上能找到一个干净的参考表。相反，这些规则分散在州税务机关的PDF文件中，格式不一致。到第一周结束时，我只覆盖了我们需要的12个州中的3个。我立刻向经理提出此事，没有等待，并提出了一个修订后的计划：在原定截止日期前交付5个优先级最高的州（覆盖80%的试点用户），剩余7个州在下周交付。我还建议银行展示一个只有这5个状态的工作演示，把它定位为分阶段推出，而不是错过。
结果：我们错过了最初的“全部12个州”截止日期。但因为我提前标记了风险，我的经理能够在演示前重新调整银行的预期，而不是演示期间。银行实际上对分阶段方案表示支持——他们表示这显示了更现实的推广计划。所有12个州都晚了一周完成。
学习：我学到错过截止日期时，如果是突发事件，情况会更糟。一旦我发现瞄准镜错了，立刻提高它就是我做的最重要的事情。我还学会了先做最难的部分原型——如果我从州税规则开始，而不是简单的上传和提取流程，我第二天就能掌握复杂性，而不是第五天。

Why so fast?
在我的创业实习期间，我们了解到一个竞争团队即将推出一款非常相似的产品，目标客户和银行合作伙伴相同。我们的CEO决定必须在税季开始前——一周内——将MVP交付，以锁定客户信任并维护我们的银行合作关系，防止竞争对手取得。”
A competitor was moving fast to target the same customers and bank partners, and launching before tax season was critical to keeping those relationships.

### 3. Gen AI
- GenAI questions can go very deep: interviewers may ask about specific tools, workflow, AI vs. traditional AI differences, and one candidate was asked to **live demo** how they use AI to solve a coding problem on a shared screen.
- 无法完成task的情况 / gen-ai mistake
ai：使用了什么ai（区别之类的），ai的信任程度？ 怎么使用ai

中間還有簡單問了一點八股，確認大概理解 Heap 定義跟 gen AI 和傳統 AI 差異
提供一个经历攒人品吧，最开始问的Gen AI,我说我在open source里用AI加快我开发速度，然后就被打断了开始问我那个project的架构，怎么处理细节， 一直问到结束，所以确实可能会被拷打
genai 被拷打简历和ai相关概念
补个genai不太常见的面经：coding做完以后还有点时间，让我share屏幕打开ide现场展示怎么用ai做这道题 我最后prompt就是把问题直接贴进去，写了我的思路，然后写了几个edge case让ai注意…
GenAI：使用的例子，如何判断AI正确还是错误，如何改进

Online Note:
上来就是顶层设计、架构决策、CLAUDE.md 配置、规范驱动开发——先把“怎么让 AI 听你话”这件事讲透。
然后一行一行代码带着你搭，后端骨架、前端工程、基础组件，
再到核心功能交付，最后容器化部署、可观测性、复盘。

**Have you ever used AI/GenAI to boost productivity in work or school? How exactly?**
I used Claude to refactor a full-stack NCAA basketball NIL valuation platform — a FastAPI backend, a React/Vite/Tailwind frontend, and an ML pipeline feeding a SQLite warehouse. 

The codebase had grown organically with a lot of technical debt: a 167-line monolithic main.py, hardcoded paths including a Windows-specific C:\Users\patey\..., 11 duplicated API URL references across frontend views, dead imports, a D1 school whitelist copy-pasted in three files, and CSS so low-opacity the text was barely readable. I used AI to plan the restructure, generate the refactored files step by step, and validate every step before moving on."

#### Common Follow-Up Directions

**Trust and judgment** — 
How do you determine if AI output is correct or wrong? 判断人工智能的输出对错？
Have you encountered a situation where AI made a mistake? AI犯过错的情况？
How do you improve or iterate on AI-generated results? 改进或迭代AI生成的结果？
This is about showing you treat AI as a tool you verify, not a black box you blindly trust.

**Specific tools and workflow** — 
Which AI tools do you use, how do you configure them (e.g., CLAUDE.md, prompting strategies), and what does your actual workflow look like from prompt to production code? 你使用哪些AI工具？如何配置它们（例如 CLAUDE.md、提示策略），从提示到生产代码的实际工作流程是怎样的？

**Technical depth on your project** — the project's architecture, implementation details, and design decisions.

**AI concepts and knowledge** — Interviewers may test whether you understand the fundamentals: 
what GenAI is vs. traditional AI
how tools like LLMs differ from classical ML models
textbook-style definitions (one candidate was quizzed on heap definitions alongside AI concepts).


### 4. **Conflict / Disagreement** — A time you had a conflict, disagreement, or different opinion with a teammate or stakeholder | 23 |
还问了一个pushback好像所以用的conflict 当时我没听懂pushback是什么 但其他句子听起来像是有矛盾？
disagree with someone else

Situation: During my internship, I was building an invoice editing feature for an internal billing management app. The staff processed a high volume of invoices daily, and I noticed that many followed similar patterns — same vendor origin, similar date ranges, billed to the same beverage company.
Task: I proposed adding a batch-edit capability so staff could update multiple similar invoices at once instead of editing them one by one, which I estimated would save significant time per billing cycle.
情况：实习期间，我为一个内部账单管理应用开发了一个发票编辑功能。员工每天处理大量发票，我注意到许多发票遵循相似模式——供应商来源相同，日期范围相似，向同一家饮料公司收费。
Action: My coworker pushed back firmly. She was worried that batch operations could corrupt the database — either through accidental user error or a malicious action wiping out many records at once. I understood her concern because data integrity is critical for a billing system. Rather than dismissing her or just dropping my idea, I took a few steps. First, I pulled usage data and confirmed that around 70% of edits followed repetitive patterns, which validated the efficiency gain. Second, I talked with my mentor about mitigation strategies. Third, I brought a revised proposal back to my coworker: we'd cap batch edits at 10 invoices at a time and implement a sync log so any batch operation could be rolled back. I walked her through how the rollback mechanism would protect the database.
任务：我提议增加批量编辑功能，让员工可以一次更新多个类似发票，而不是逐个编辑，我估计这将为每个计费周期节省大量时间。
动作场面：我的同事坚决反驳。她担心批处理可能会破坏数据库——无论是用户意外失误，还是恶意行为一次性清除大量记录。我理解她的担忧，因为数据完整性对计费系统至关重要。我没有否定她，也没有放弃我的想法，而是迈出了几步。首先，我提取了使用数据，确认大约70%的编辑遵循重复模式，验证了效率提升。其次，我和导师讨论了缓解策略。第三，我把修改后的提案带回给同事：批量编辑次数限制在每次10个发票，并实施同步日志，以便任何批次操作都能回滚。我向她讲解了回滚机制如何保护数据库。
Result: We agreed on the revised design, shipped it within the sprint, and the billing team gave positive feedback — their workflow was noticeably faster. There were zero data incidents after launch because the safeguards worked as intended.
结果：我们就修订设计达成一致，在冲刺内发布，计费团队也给出了积极反馈——他们的工作流程明显加快了。发射后没有发生任何数据事件，因为安全措施按预期运作。
Learn: I learned that when someone pushes back, their underlying concern is usually valid even if I disagree with their conclusion. By treating the pushback as a constraint to design around rather than an obstacle to overcome, I ended up with a stronger feature than my original proposal.
学习：我学到，当有人反驳时，他们的内在担忧通常是合理的，即使我不同意他们的结论。通过将阻力视为设计的限制，而非必须克服的障碍，我最终得到了比最初提案更强的功能。

故事2：替代方案——对API设计方法的分歧
情况：在后端团队实习期间，我被要求构建一个REST API端点，该端点能为内部仪表盘返回筛选搜索结果。团队中的另一名实习生正在开发将消耗该API的前端。
任务：我们对过滤机制的运作方式存在分歧。我想在后端用查询参数来处理过滤，让 API 只返回所需的内容——减少负载大小并保持逻辑集中管理。另一位实习生希望API能返回所有数据，并在前端用JavaScript进行过滤，认为这样界面响应更灵敏，因为过滤更改时不需要额外的网络调用。
动作场面：我建议我们各自花半天时间做初步原型，然后进行比较。我构建了后端过滤版本并测量了响应时间。他构建了客户端过滤版本。对比时，客户端方法对小数据集效果不错，但导师指出，数据在生产中将扩展到数千条记录，将所有数据传输到浏览器会成为性能和安全问题。同时，我也承认即时筛选切换的用户体验确实更好，所以我在前端添加了一个轻量级缓存层，用于最新的查询结果，给我们提供了他想要的响应性，而无需发送完整数据集。
结果：我们发货的是混合方案。即使在大规模情况下，仪表盘加载也很高效，团队负责人在我们的冲刺评审中特别赞扬了缓存的想法，说这是我们单独无法实现的。
学习：我了解到，解决技术分歧的最佳方式是让数据自己发声。当双方都进行原型设计和测量，而不仅仅是抽象争论时，正确答案通常变得显而易见——而且往往是两者的结合。

## Tier 2: High Frequency

5. **Harsh / Negative / Tough Feedback** — A time you received harsh or negative feedback and how you dealt with it | 13 |

6. **Challenging Project / Complex Problem** — Describe a challenging project or complex problem you worked on | 12 |
obstacle：第一个故事比较technical，问了followup，后续又讲了一个interpersonal skill的故事
-> 2Wind

7. **Help Peers**
探探你可能与同事的一些互动，告诉我有一次你决定介入并提供帮助
follow up-你是怎么决定介入并且help的
从长远来看 你有帮助他们么，在解决这个事情以后 他们有什么提升么

new hire ramp up on codes
first provide docs and onboarding seems fine
assign him a frontend page, but got delayed for days
since i am the full-stack here and used to work on frontend dev, my responsibility to ensure product delivery
I proactively ask and set 1-on-1 with him
the new hire says his problem and say he was intimiate to ask as do not want to waste other's time
I help fix
share debug / tutorial
weekly update with me and encourage to ask
he completed ramp-up plan
manager happy
formalize peer mentor rules for future new hire
learn: proactive observe problems, good for work environment and boost working efficiency

## Tier 3: Moderate Frequency

| # | Question Topic | Count |
|---|---------------|-------|
| 7 | **Resume Deep-Dive** — Detailed follow-ups on resume projects (tech stack choices, architecture decisions, user count, trade-offs, project details) | 4 |
| 8 | **Deliver Results** — A time you delivered results under pressure or met a goal | 4 |
| 9 | **Obstacle / Unexpected Changes** — Obstacles in a project, unexpected pivot, or change of direction mid-project | 4 |
| 10 | **Failure / Missed Deadline** — A time you failed, made a mistake, or missed a deadline, and what you learned | 3 |
| 11 | **Proud Project / Biggest Achievement** — A project you are most proud of or the biggest thing you've done | 3 |
| 12 | **Explore Unknown / Learn Quickly** — A time you had to learn something new or explore unfamiliar knowledge | 2 |
| 13 | **Earn Trust** — A time you earned trust from your team or stakeholders | 2 |

## Tier 4: Mentioned Once or Twice

| # | Question Topic | Count |
|---|---------------|-------|
| 14 | **Outside Your Responsibilities / Out of Scope** — A time you took on work outside your scope | 2 |
| 15 | **Efficiency / Simplify** — A time you simplified a process or improved efficiency | 1 |
| 16 | **Big Decision** — A time you had to make a big or impactful decision | 1 |
| 17 | **Creativity** — A time you came up with a creative solution | 1 |
| 18 | **Metrics-Based Problem Solving** — How you used metrics or data to solve a challenge | 1 |
| 19 | **Scenario-Based BQ** — Pure situational questions where pre-prepared stories don't apply | 1 |

---
