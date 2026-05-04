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

**Situation:**
During my previous internship, the team was building a trading platform for college football players where prices are driven by real game data. 
I was working on ingesting player's seasonal data into PostgreSQL through an ingestion pipeline. 
After running the pipeline for a small group of college teams during dev environment, I noticed some players had multiple season aggregates for the same year. 
Season aggregates are like a year summary — there should only be one per player per year. 
And that meant the pipeline wasn't idempotent even though it used the upsert logic with a unique constraint.

**Task:**
Soon as I realized, I notified the team. 
My mentor confirmed this should be top priority, so I took full ownership of diagnosing and fixing the pipeline, as our main product depends on accurate game data.

**Action:**
I started by running queries to find all players with more than one season aggregate for the same year. 
By pulling those duplicated rows side by side, I noticed that the same player had different team IDs among those duplicates, which happened when players transfer teams in mid-seasons. 
Because team_id was part of the unique constraint, upset treated those data as a new record instead of an update. 

Next, I took a closer look at the stats table, looking for another field that is unique and not changing over time.
And I found the game_id field, which was NULL for all season aggrgates. 
If I replaced the team_id with game_id, the unique constraint became: player_id, game_id, season, category, and source_id -- which should remove the duplicates no matter which team the player was in.

But when I reran the pipeline to validate, I still saw duplicate season aggregates. 
By digging into the PostgreSQL docs, I realized the issue: season aggregates had NULL in game_id, and PostgreSQL treats NULL ≠ NULL by default, so two NULLs would never trigger a conflict — both rows just got inserted. 
I brought this to my mentor, and he pointed me to PostgreSQL 15’s feature: NULLS NOT DISTINCT, which treats NULL as equal for constraint purpose.
After that, we discussed the solution with the tech lead, confirming it was safe to modify the existing constraint and applied the change.

**Result:**
After the applying the fix, rerunning the pipeline produced no duplicates or data loss. 
This was critical because player data directly drove the price evaluations at the core of our product.

**Learn:**
From this experience, I learned that mistakes are often hide in the assumption, and it is important to challenge those preset assumptions.
Now when I design any upsert logic, I always test the assumption first: which fields in the constraint could change over time? Are there edge cases like NULLs that break the guarantee? 
That pattern helped me catch a similar issue in another table during other project.

Also, my mentor’s suggestion saved me hours of debugging, which taught me that reaching out early is faster than working hard alone.​​​​​​​​​​​​​​​​


> Q1: "How did you actually find the root cause? Did you run SQL queries, look at logs, or what?"
问1：“你是怎么找到根本原因的？你有运行SQL查询、查看日志，还是别的什么？”
Run the pipeline against a small sample first and manually inspect the rows in Supabase. Write a simple count-and-checksum test: count records in the API response, count rows inserted, and compare. Run the pipeline twice on the same data and verify no duplicates appear (this tests your upsert logic). Check edge cases yourself: what happens with null optional fields, empty arrays, Unicode text, or timestamps in unexpected formats.

是的，这一切始于一个简单的计数查询。运行了两次管道后，我运行了类似寻找重复行的程序。那给了我一份有重复角色的球员名单。然后我拉出了其中几位球员的整行，并并排对比——同一个球员，同一赛季，但球队ID不同。那时他才恍然大悟：这些人是转会球员。team_id是独特限制的一部分，所以当它变更时，Upsert将其视为新纪录。SELECT player_id, season, COUNT(*) FROM stats GROUP BY player_id, season HAVING COUNT(*) > 1
关于第二个问题——每场比赛统计覆盖赛季总数据——我发现有些赛季总数据行的数字异常具体，看起来像单场比赛统计。我查询了哪些行game_id为NULL（聚合），并与源API实际返回的行进行了比较。数字不匹配。这告诉我，每场比赛的行覆盖了聚合，因为约束无法区分它们。

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

Situation: 
During my previous internship at a startup, we needed to deliver a full-stack MVP — a tax filing platform for sports players — in two weeks. 
The product had to go live before tax season to preserve trust with our customers and bank partners. 
Missing that window would potentially lose those relationships.

Task: 
As a full-stack developer, I was responsible for shipping frontend pages along with backend API services within the tight time window.

Action: 
Understanding the urgency, I started by listing every feature the stakeholders had requested, then had a meeting with the manager to prioritize them.
The time was tight, so I decided to focus on the most crucial functionalities. 
After that, we identified three core features to be presented in the MVP — user registration, document upload, and a tax dashboard with step by step guidance for tax filling.
Other features like notifications were deferred in the later sprint.

Next, I talked with my mentor and discovered we had reusable UI templates and file-upload modules from previous internal projects, which saved me hours of work. 
I also set up daily standups to sync each member’s progress and remove any potential road blocks quickly. 

For the architectural tradeoff,
Instead of building a separate backend from scratch (like setting database, building authentication systems, and configuring file storage), I chose Supabase, which provided existing tools ready-to-go.
That allowed me to focus on the business logic to provide intuitive tax filing workflow and frontend for smooth user experience. 

By the start of second week, I had a working version deployed, and we used the rest time for live testing with pilot users.

Result: 
Eventually, we launched on time before tax season.
The pilot customer could uploaded their documents and walked through the full tax filing procedure, and our bank partner was pleased for the MVP demo.
Overall, this on-time delivery helped the startup develop a stronger relationship with both customers and partner organizations.

Learn: 
From this experience, I learned the importance of thorough planning, effective prioritization, and continuous communication within teams. 
Instead of building everything at once, prioritizing core feature and delaying lower-priority ones makes fast delivery possible without sacrificing user experience.
I also learned to proactively seek out existing resources before building from scratch, which could save significant time and reduce delay risks.


Miss the DDL Case:
“错过截止日期”报道——发布后税务计算功能
情况：在我们按时发布了报税平台的MVP后，下一个冲刺目标是在两周内添加自动化税务计算引擎。我的经理把这个时间表交给了合作银行，因为他们想向合规团队演示完整的工作流程。
任务：我拥有计算模块——负责处理上传的文件、提取收入字段，并根据玩家所在州的居住地计算预估税负。
动作场面：我低估了它的复杂性。每个州对运动员收入分配有不同的规定，我原以为网上能找到一个干净的参考表。相反，这些规则分散在州税务机关的PDF文件中，格式不一致。到第一周结束时，我只覆盖了我们需要的12个州中的3个。我立刻向经理提出此事，没有等待，并提出了一个修订后的计划：在原定截止日期前交付5个优先级最高的州（覆盖80%的试点用户），剩余7个州在下周交付。我还建议银行展示一个只有这5个状态的工作演示，把它定位为分阶段推出，而不是错过。
结果：我们错过了最初的“全部12个州”截止日期。但因为我提前标记了风险，我的经理能够在演示前重新调整银行的预期，而不是演示期间。银行实际上对分阶段方案表示支持——他们表示这显示了更现实的推广计划。所有12个州都晚了一周完成。
学习：我学到错过截止日期时，如果是突发事件，情况会更糟。一旦我发现瞄准镜错了，立刻提高它就是我做的最重要的事情。我还学会了先做最难的部分原型——如果我从州税规则开始，而不是简单的上传和提取流程，我第二天就能掌握复杂性，而不是第五天。

Why so fast?
在我的创业实习期间，我们了解到一个竞争团队即将推出一款非常相似的产品，目标客户和银行合作伙伴相同。我们的CEO决定必须在税季开始前——2周内——将MVP交付，以锁定客户信任并维护我们的银行合作关系，防止竞争对手取得。”
A competitor was moving fast to target the same customers and bank partners, and launching before tax season was critical to keeping those relationships.

What would you do differently if you had more time?
如果时间长，我会用自定义端点替换一些Supabase自动生成的API——例如，税务计算逻辑最终需要比自动生成的REST层更复杂的查询和验证。

### 3. Gen AI
- GenAI questions can go very deep: interviewers may ask about specific tools, workflow, AI vs. traditional AI differences, and one candidate was asked to **live demo** how they use AI to solve a coding problem on a shared screen.
- 无法完成task的情况 / gen-ai mistake
ai：使用了什么ai（区别之类的），ai的信任程度？ 怎么使用ai

中間還有簡單問了一點八股，確認大概理解 Heap 定義跟 gen AI 和傳統 AI 差異
提供一个经历攒人品吧，最开始问的Gen AI,我说我在open source里用AI加快我开发速度，然后就被打断了开始问我那个project的架构，怎么处理细节， 一直问到结束，所以确实可能会被拷打

Online Note:
上来就是顶层设计、架构决策、CLAUDE.md 配置、规范驱动开发——先把“怎么让 AI 听你话”这件事讲透。
然后一行一行代码带着你搭，后端骨架、前端工程、基础组件，
再到核心功能交付，最后容器化部署、可观测性、复盘。

**Have you ever used AI/GenAI to boost productivity in work or school? How exactly?**
Situation
I took over a full-stack analytics platform from a capstone team. The ML pipeline was valuable, but the frontend was unreadable and the backend was a flat monolithic structure — hard for any future developer to maintain or build on.

Task
Refactor frontend (React) and backend (FastAPI) into a clean, maintainable architecture using AI, without breaking any existing functionality or touching the ML pipeline.
我接手了一个顶点团队的全栈分析平台。机器学习流水线很有价值，但前端难以读取，后端则是一个扁平的整体结构——对未来的开发者来说很难维护或开发。
任务
利用AI重构前端（React）和后端（FastAPI），将其重构成一个干净、可维护的架构，同时不破坏任何现有功能，也不涉及机器学习流水线。

Action
**Spec first.** Before involving AI, I manually read through the codebase and wrote markdown spec files defining: target architecture, naming conventions, and explicit constraints — especially what AI should NOT do (don't modify the ML pipeline, don't change API response field names or formula weights). I included relevant spec sections in every AI prompt to prevent violations upfront, and reviewed output against them as a second check.

**Tests to lock in existing behavior.** Before changing any code, I wrote tests against the existing API endpoints capturing current responses — exact fields, types, and values. This is the safety net that proves refactoring changed structure without changing behavior. AI helped generate test scaffolding, but I wrote every assertion myself because the assertions are the specification.

**One module at a time with structured prompts.** I refactored in dependency order — backend first (config → schemas → services → routes), then frontend (API client → hooks → components → styling). For each step, I gave AI only the relevant files for that step plus the spec constraints, not the entire codebase. Each prompt defined the purpose, expected inputs/outputs, and edge cases.

**Verify before committing.** After every AI-generated module, I checked the diff against the original to catch unnecessary changes or hallucinated imports, ran the test suite, then committed. One module, one commit. When something broke — for example, AI generated import paths that didn't match the new package structure — I caught it by running the server, pasted the traceback back to AI with the directory layout, and we fixed it collaboratively.

先设定。在引入AI之前，我手动阅读了代码库，编写了markdown规范文件，定义了目标架构、命名规范和显式约束——尤其是AI不应该做的事情（不要修改机器学习流水线，不要更改API响应字段名称或公式权重）。我在每个AI提示中都包含相关的规格章节，以防止违规，并对输出进行第二次检查。
测试来锁定已有的行为。在更改任何代码之前，我会针对现有API端点编写测试，捕捉当前响应——精确字段、类型和值。这就是证明重构结构变化而不改变行为的安全网。AI帮助生成了测试支架，但每一条断言都是我自己写的，因为断言本身就是规范。
一次只模块，提示有结构化。我按依赖顺序重构——先后端（配置→模式→服务→路由），然后是前端（API客户端→钩子→组件→样式）。对于每一步，我只给了 AI 该步骤相关的文件和规范约束，而不是整个代码库。每个提示词都定义了目的、预期输入/输出和边缘情况。
承诺前先核实。每次AI生成的模块后，我都会对比原始模块的差异，以发现不必要的更改或误导入，运行测试套件，然后提交。一个模块，一个提交。当出现故障——比如AI生成的导入路径与新包结构不符——我通过运行服务器发现问题，将追踪回贴到目录布局中粘贴给AI，我们合作修复了它。

Result
Done in three days. Clean layered architecture on both sides, all existing functionality preserved, any new developer could ramp up quickly.

Learn
Have AI show its plan before generating code. Early on I went straight to "generate the refactored file" and sometimes got code that violated a constraint I hadn't stated in that particular prompt. Switching to "what would you change and why — no code yet" let me catch misalignments before any code was written. Better planning upfront always beats fixing output after the fact.

结果
三天内完成。两侧架构干净分层，所有现有功能都保留，任何新开发者都能迅速启动。
学习
让AI在生成代码前先展示它的计划。早期我直接“生成重构文件”，有时会遇到违反我未在提示中说明的约束的代码。切换到“你会改变什么以及为什么——还没有代码”，让我能在任何代码写好之前发现不对齐。提前做好规划总比事后修正输出更重要。

#### Common Follow-Up Directions
**Workflow**
1. Understand requirements
2. Define the target architecture, naming conventions, constraints, why certain decisions, and what AI should NOT do. Storing in markdown files in a dedicated folder.
3. Test-driven: Write or confirm tests before code
4. Structured Prompt: define purpose, expected format of inputs/outputs, and edge cases
Relevant spec context in the prompt 
Update one module at a time instead of complete refactoring at once
5. Review Output: check the diff against the original, and check for things tests won't catch (wrong imports or unnecessary changes)
6. Run Tests
7. Commit to repo

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

Situation: 
During my internship, I was working on an invoice editing feature for an internal billing management tool. 
The financial team processed high volumes of invoices each day, and I noticed that many followed similar patterns — same pickup location, similar date ranges, billed to the same beverage company.

Task: 
Therefore, I proposed to add a batch-edit function so the financial team could update multiple invoices at once instead of editing them one by one, which should save significant time per billing cycle.

Action: 
However, my coworker pushed back firmly. 
She was worried that batch operations could corrupt the database — either through accidental error or malicious actions of wiping out records at once. 

I understood her concern because data integrity is critical for a billing system. Instead of dismissing her or just dropping my idea, I made some studies. 

First, I pulled invoice data and confirmed that around 70% of edits followed the same patterns — same manufacturer/ location/ billing party, which confirmed the potential to improve.

Second, I talked with my mentor about safeguard strategies, seeking for his suggestions to balance security concerns and user efficiency.
After observing the client’s workflow and UI layout, I decided to limit the amount of invoices can be edited together to 10, and implement a sync log so any batch operation can be rolled back.

Third, I brought a revised proposal back to my coworker.
By walking her through how the edit amount limitation and the rollback mechanism would protect the database, we both agreed on the updated plan.

Result: 
As a result, the batch edit feature was shipped within the sprint.
The billing team gave positive feedbacks, as their workflow became noticeably faster.
There were no data incidents after launch and the safeguards worked as intended.

Learn: 
From this experience, I learned to keep an open mind to pushbacks.
Even if I disagree, different opinions could reflect concerns that I overlooked.
By treating them as a constraint to design rather than an obstacle to overcome, I ended up with a stronger feature than my original proposal.

故事2：替代方案——对API设计方法的分歧
情况：在后端团队实习期间，我被要求构建一个REST API端点，该端点能为内部仪表盘返回筛选搜索结果。团队中的另一名实习生正在开发将消耗该API的前端。
任务：我们对过滤机制的运作方式存在分歧。我想在后端用查询参数来处理过滤，让 API 只返回所需的内容——减少负载大小并保持逻辑集中管理。另一位实习生希望API能返回所有数据，并在前端用JavaScript进行过滤，认为这样界面响应更灵敏，因为过滤更改时不需要额外的网络调用。
动作场面：我建议我们各自花半天时间做初步原型，然后进行比较。我构建了后端过滤版本并测量了响应时间。他构建了客户端过滤版本。对比时，客户端方法对小数据集效果不错，但导师指出，数据在生产中将扩展到数千条记录，将所有数据传输到浏览器会成为性能和安全问题。同时，我也承认即时筛选切换的用户体验确实更好，所以我在前端添加了一个轻量级缓存层，用于最新的查询结果，给我们提供了他想要的响应性，而无需发送完整数据集。
结果：我们发货的是混合方案。即使在大规模情况下，仪表盘加载也很高效，团队负责人在我们的冲刺评审中特别赞扬了缓存的想法，说这是我们单独无法实现的。
学习：我了解到，解决技术分歧的最佳方式是让数据自己发声。当双方都进行原型设计和测量，而不仅仅是抽象争论时，正确答案通常变得显而易见——而且往往是两者的结合。

## Tier 2: High Frequency

### 5. **Harsh / Negative / Tough Feedback** — A time you received harsh or negative feedback and how you dealt with it | 13 |

Situation: During my internship on a frontend team, I was assigned to build a tab navigation system — similar to how browser tabs work — for one of our internal tools. I was relatively new to the codebase and the team.
Task: Deliver the tab component within the sprint. The expectation was that it would be a fairly quick task given the team's existing patterns.
情况：在前端团队实习期间，我被分配为我们内部的一个工具构建一个标签页导航系统——类似于浏览器标签的工作原理。我当时对代码库和团队还比较新。
任务：在冲刺中交付标签组件。考虑到团队现有的模式，预计这将是一项相当快速的任务。
Action: I spent three days building the component from scratch. When my manager saw the timeline, he was direct: this shouldn't have taken that long. He pointed out that other engineers on the team had built similar UI patterns before, and I should have looked at their work and reused those patterns instead of starting from zero. My first reaction was frustration with myself — he was right, and I realized I'd been heads-down coding without looking around. I reflected on why it happened: I wasn't plugged into the team's existing knowledge. So I made concrete changes. I started paying close attention during standups to understand what others were working on and what already existed. I actively volunteered for code reviews, which forced me to read other people's code and learn the codebase faster. I also started reading design docs for features outside my immediate tasks. A few weeks later, when I picked up a product search bar feature with filtering, I recognized that another team had built similar filtering logic. I reached out, collaborated with them, and reused their approach — delivering the feature significantly faster than if I'd built it alone.
动作场面：我花了三天时间从零开始构建这个组件。当我的经理看到时间表时，他很直接地说：这本不该花那么久。他指出团队里其他工程师之前也做过类似的UI模式，我应该看看他们的工作并重复使用那些模式，而不是从零开始。我第一反应是对自己感到沮丧——他说得对，我意识到自己一直在埋头苦写代码，没怎么看周围。我反思了为什么会这样：我没有连接到团队已有的知识。所以我做了具体的改变。我开始在单口喜剧中密切关注别人在做什么，哪些已经存在。我主动参与代码审查，这迫使我更快阅读别人的代码并学习代码库。我还开始阅读设计文档，针对我当前任务之外的功能。几周后，当我使用带有筛选功能的产品搜索栏功能时，我发现另一个团队也构建了类似的过滤逻辑。我联系了他们，与他们合作，并重新采用了他们的方法——比我单独开发时更快地交付了功能。
Result: The search bar feature shipped ahead of schedule, and the cross-team collaboration set a pattern that other engineers started following. My manager specifically called out the cross-team impact during my review and noted the improvement from where I'd started.
结果：搜索栏功能提前发布，跨团队协作形成了其他工程师开始效仿的模式。我的经理在评估时特别指出了跨团队的影响，并指出我比起点有很大进步。
Learn: I learned that engineering efficiency isn't just about how fast you code — it's about how well you leverage the people and resources around you. Since then, my first step on any new task is to ask "has anyone solved something like this before?" before writing a single line of code.
学习：我了解到，工程效率不仅仅是编码速度，更在于你如何善用周围的人和资源。从那以后，我每次做新任务的第一步，都是在写一行代码前先问“有人解决过类似的问题吗？”。

### 6. **Challenging Project / Complex Problem** — Describe a challenging project or complex problem you worked on | 12 |
obstacle：第一个故事比较technical，问了followup，后续又讲了一个interpersonal skill的故事
-> 2Wind

### 7. **Help Peers**
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
### 7 | **Resume Deep-Dive** — Detailed follow-ups on resume projects (tech stack choices, architecture decisions, user count, trade-offs, project details) | 4 |
### 8 | **Deliver Results** — A time you delivered results under pressure or met a goal | 4 |
### 9 | **Obstacle / Unexpected Changes** — Obstacles in a project, unexpected pivot, or change of direction mid-project | 4 |
### 10 | **Failure / Missed Deadline** — A time you failed, made a mistake, or missed a deadline, and what you learned | 3 |
Batch edit -> more complex, security concern -> enable single first then batch

### 11 | **Proud Project / Biggest Achievement** — A project you are most proud of or the biggest thing you've done | 3 |
### 12 | **Explore Unknown / Learn Quickly** — A time you had to learn something new or explore unfamiliar knowledge | 2 |
### 13 | **Earn Trust** — A time you earned trust from your team or stakeholders | 2 |

### 14 | **Outside Your Responsibilities / Out of Scope** — A time you took on work outside your scope | 2 |
search bar not functioning -> customer experience, vue2

### 15 | **Efficiency / Simplify** — A time you simplified a process or improved efficiency | 1 |
player mapping layer -> just log and insert if 3-tier fail

### 16 | **Big Decision** — A time you had to make a big or impactful decision | 1 |
### 17 | **Creativity** — A time you came up with a creative solution | 1 |
### 18 | **Metrics-Based Problem Solving** — How you used metrics or data to solve a challenge | 1 |
### 19 | **Scenario-Based BQ** — Pure situational questions where pre-prepared stories don't apply | 1 |

---
