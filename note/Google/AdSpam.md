## Email Info
30-minute team match call
Manager: Arda
Location: Mountain View, CA 94043
Team Description:

Join our fight against spam and use your ingenuity to outsmart those who seek to undermine Google Search Ads!
AdSpam, externally known as the Ad Traffic Quality group, is part of the Ads Privacy & Security org. Our mission is two-fold: to protect our global ad networks from billions in fraud and invalid activity, and to fiercely shield the advertiser trust at the very heart of Google’s platforms. We play an instrumental role in ensuring the long-term sustainability of the digital ads ecosystem, and ultimately, the free internet!

We are a diverse group of engineers, analysts, product & program managers, and researchers, collaborating cross-functionally to tackle complex, large-scale problems in the fight against invalid traffic (IVT). We work on some of the largest data sets in the world, build sophisticated detection systems, and apply state-of-the-art ML models. AI/Agent technologies are crucial in helping us scale our defenses and stay ahead of constantly evolving attacks.

## 1. Team's Background

**Invalid Traffic (IVT)**: 来自不真正有兴趣的用户的activity

1. General IVT (GIVT)
*Known* bots and crawlers -> filter using denylists
2. Sophisticated IVT (SIVT)
Hard to identify -> require more in-depth analysis

Attack Type:
- Botnets: 假用户 / automated programs running on servers or hijacked computers to mimic real-user behavior
Behavior：打开网页, 滚动页面, 点击广告, 模拟停留时间 / 鼠标移动 / 浏览路径
目的: 刷点击（Click Fraud）, 刷展示（Impression Fraud）, 消耗广告主预算

- Clickjacking: 欺骗用户点击 / deceptive UI elements that trick users into clicking ads they didn't intend to

- Falsely represented inventory: 僞裝广告来自“高价值流量” / misrepresent traffic sources
Ad traffic disguised as coming from high-value users or premium sites
网站伪装（Domain Spoofing）: 广告交易平台看到nytimes.com, 实际展示在spammy-site-123.com
用户质量伪装: 声称是-美国用户/高消费人群, 实际是-低价值地区/机器人
目的: 把“低价流量”卖成“高价流量”

- Hidden ads / pop-unders: 广告被加载了，但用户没看到 / deceptive ad delivery
served in the background without user awareness
目的: 刷 impression（展示量）, 不影响用户体验（避免被发现）


**Why it matters to advertisers**
Enormous financial stakes. 

For advertisers, every fraudulent click directly drains their budget without any business value. 耗尽预算，却没有商业价值。
For publishers, IVT undermines the revenue of legitimate content creators. 扭曲市场，削弱收入

So Arda's team description emphasizes "shielding the advertiser trust at the very heart of Google's platforms".
If advertisers lose confidence that their spend reaches real humans, the entire ad-funded internet model breaks down.
如果广告主失去对其消费触及真实用户的信心，整个广告资助的互联网模型就会崩溃。

**Why this problem is hard (adversarial, massive scale, real-time)**
1. Attackers continuously adapt. 攻击者并不断调整
Fraudsters reverse-engineer detection signals, program bots to mimic human browsing patterns. 逆向工程检测信号，bot模仿人类浏览模式

2. Massive scale. 大规模 -> Latency
You need detection that works in real time or near-real time on this volume. 
Google uses over a hundred complex algorithms to spot bad traffic as it happens. Some filtering must occur pre-bid (before an ad is even purchased), while other patterns only emerge over days or weeks of observation. This means multi-layered systems with varying latency requirements. 
你需要对该体积进行实时或近实时的检测。谷歌使用一百多种复杂算法来及时识别不良流量。有些过滤必须在竞标前（甚至在广告购买前）进行，而其他模式则仅在几天或几周的观察中显现。这意味着多层系统具有不同的延迟需求。

3. Precision. 
The team must avoid both false negatives (letting fraud through, costing advertisers money) and false positives (filtering legitimate traffic, which harms publishers and reduces ad revenue). 必须避免假阴性（让欺诈通过，给广告主带来损失）和假阳性（过滤合法流量，损害出版商并减少广告收入）。


近期的人工智能/大型语言模型创新（很好的话题）
In August 2025, Google published a blog post about the Ad Traffic Quality team partnering with Google Research and DeepMind to apply large language models to IVT detection. 谷歌发布了一篇关于广告流量质量团队与谷歌研究院和DeepMind合作，将大型语言模型应用于IVT检测的博客文章。


## **2. Prepare your "why this team" story**

This is probably the single most important thing in a team match. Have a clear, genuine answer for why fraud/abuse detection excites you. Connect it to something specific in your background — your experience building pipelines that handle messy, unreliable data, or the adversarial thinking you applied when preventing flash-sale abuse, for example. Avoid generic answers like "I want to work on large-scale systems."

Let me review your resume details more carefully to craft the strongest connections.

Looking at your resume alongside the team's mission, here are the most compelling connections you can draw — and how to weave them into a natural "why this team" narrative.

---


### 1. Flash-Sale Abuse Prevention → Adversarial Thinking at Scale

Your **Distributed eCommerce Platform** project is your single best parallel. You built defenses against a fundamentally adversarial problem: preventing overselling during flash sales where bad actors (or just overwhelming traffic) can exploit race conditions. Specifically, you used Redis request gating, optimistic locking, and Kafka-based async processing to handle traffic bursts — this is the same *pattern* as IVT defense: you need to make fast, high-volume decisions about which requests are legitimate and which should be blocked, all under extreme time pressure and with financial consequences for getting it wrong.

**How to say it:** *"In my flash-sale system, I had to gate requests in real time and decide which ones to let through under enormous concurrency pressure — and the cost of a false negative was real money lost to overselling. That's a miniature version of what Ad Traffic Quality does: making high-stakes filtering decisions at massive throughput where both letting bad traffic through and accidentally blocking good traffic have direct financial impact."*

### 2. Data Pipeline Engineering → Processing Trillions of Events

At **Second Wind AI**, you migrated 16K+ player profiles and 72K+ game records, redesigned schemas to eliminate duplicates, and built idempotent ingestion pipelines. At **CLYNK**, you reworked SQL schemas to cut query latency by 40% across 5,000+ products. Arda's org processes trillions of events daily — the infrastructure half of his team builds and maintains exactly these kinds of high-throughput data systems. Your experience designing for idempotency, deduplication, and schema optimization shows you understand the data engineering discipline required when operating on unreliable, messy, high-volume data.

**How to say it:** *"I've spent a lot of time thinking about data integrity at the pipeline level — making ingestion idempotent, eliminating duplicate records, designing schemas that support efficient cross-dimensional queries. Arda's team processes trillions of events per day, and I know from experience that the quality of detection is only as good as the reliability and design of the data infrastructure underneath it."*

### 3. OnCall Automation Agent → AI/Agent Technologies

The team description explicitly calls out that "AI/Agent technologies are crucial in helping us scale our defenses." Your **OnCall Automation Agent** project is a direct proof point: you built a multi-agent system orchestrating RAG pipelines, ReAct chat agents, and Plan-Execute-Replan workflows. You also integrated MCP tool calling with Prometheus, logs, MySQL, and web query tools — essentially teaching an AI agent to pull telemetry and take action. This maps naturally to the team's use of LLMs and agent-based approaches to detect and respond to invalid traffic patterns.

**How to say it:** *"I noticed the team is increasingly leveraging AI and agent technologies — I saw the blog post about using LLMs for content review. I built an OnCall automation agent that orchestrates multiple AI workflows to analyze alerts, query knowledge bases and metrics, and generate remediation steps. The idea of applying that kind of agentic reasoning to fraud detection, where the system has to autonomously analyze patterns and decide how to respond, is exactly the kind of work I want to do."*

---

## Putting It All Together: Your "Why This Team" Narrative

Here's a draft you can adapt in your own voice:

> *"What draws me to this team specifically is that it sits at the intersection of three things I care most about: building reliable infrastructure that handles data at scale, adversarial problem-solving where the requirements keep shifting, and applying AI to automate complex decision-making. In my projects, I've built real-time gating systems to prevent abuse during flash sales, designed idempotent pipelines to ensure data integrity across messy sources, and architected multi-agent AI systems for automated diagnostics. Ad Traffic Quality combines all of those — you're processing trillions of events, the adversaries are constantly adapting, and the team is pushing into LLM and agent-based approaches to stay ahead. I find that combination genuinely exciting because you never get to stop learning — the problem evolves every day."*

---

## What to Avoid

Don't lean on generic motivations like "I want to work at Google scale" or "I'm interested in ML." Instead, stay concrete and personal. If Arda asks a follow-up like "What specifically interests you about fraud detection?", you can go deeper on the adversarial angle: *"I like that you can't just build a solution and walk away — the attackers adapt, so the engineering has to keep evolving too. That feedback loop between detection and evasion is the kind of problem that keeps me engaged."*

Would you like me to help you prepare for the next question on your list?








## **3. Have 2–3 projects ready to discuss at depth**

Pick projects that resonate with their work. I'd recommend your distributed eCommerce platform (shows scale thinking, concurrency, Redis/Kafka), your OnCall Automation Agent (shows AI/agent experience, which they explicitly value), and your CLYNK billing work (shows real production impact with data optimization). For each, be ready to explain the problem, your design decisions, tradeoffs you considered, and what you'd do differently.

## **4. Prepare 3–4 thoughtful questions for Arda**

This signals genuine interest and fills the back half of the call naturally. Some ideas: How is the team incorporating AI/agent technologies into detection workflows? What does the balance between automated defenses and human review look like? What's the biggest technical challenge the team is facing right now? What does onboarding and ramping up look like for a new engineer?

## **5. Brush up on basic fraud detection concepts**

You don't need deep expertise, but knowing terms like invalid clicks, click fraud, bot detection, anomaly detection, and class imbalance will help you follow the conversation and ask smarter follow-up questions. Spend 30–60 minutes reading overview material.

## **6. Know your resume cold**

Arda will have your resume in front of him. Make sure you can speak to every bullet point without hesitation, especially the numbers you cited (20% load time improvement, 40% query latency reduction, 16K+ player profiles). Know the "so what" behind each metric.

## **7. Logistics and tone**

Be conversational, not rehearsed. Team match calls are bidirectional — Arda is selling the team to you too. Show curiosity by reacting to what he shares and asking natural follow-ups rather than just running through a script. Have a quiet space, stable connection, and join a minute early.

Items 1–4 are where you should spend the bulk of your prep time. Items 5–7 are important but take less effort. Good luck — your background maps well to what this team needs.