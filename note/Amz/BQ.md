## Notes
- Common Follow-up: why, trade-offs, how you measured success, etc.
- Prepare **7+ stories** for: Fail/Mistake, Outside Responsibilities, Tight Deadline, Gen AI, Challenging Project, Conflict, and Deep Dive.


## Tier 1: Very High Frequency
### 1. Deep Dive
A time you had to deep dive into a problem or topic / find the root cause / analyze a bug + 追问拷打
建議有在準備的好好想一下，這題比較像你解決一個bug 或是 service 壞掉，你怎麼找到root cause
dive deep root cause + follow up
dive deep root cause wasn't obvious problem, but you found out -> follow-up: how do you find that out
follow up- dive deep：怎么弄优先级 如果你已经弄了12task 还剩34怎么办
### 2. Tight Deadline
2. **Tight Deadline** — How you handled a tight deadline or delivered under time pressure / 没有完成的情况 | 24 |
Follow-up: 花了多长时间交付 是否做出牺牲

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

## Tier 2: High Frequency

5. **Harsh / Negative / Tough Feedback** — A time you received harsh or negative feedback and how you dealt with it | 13 |

6. **Challenging Project / Complex Problem** — Describe a challenging project or complex problem you worked on | 12 |
obstacle：第一个故事比较technical，问了followup，后续又讲了一个interpersonal skill的故事

7. **Help Peers**
探探你可能与同事的一些互动，告诉我有一次你决定介入并提供帮助
follow up-你是怎么决定介入并且help的
从长远来看 你有帮助他们么，在解决这个事情以后 他们有什么提升么

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
