## Email Info
3-min -> half swe half data enineer
sql
signal building
ML / Python
residential proxy


30-minute team match call
Manager: Arda
Location: Mountain View, CA 94043
Team Description:

Join our fight against spam and use your ingenuity to outsmart those who seek to undermine Google Search Ads!
AdSpam, externally known as the Ad Traffic Quality group, is part of the Ads Privacy & Security org. Our mission is two-fold: to protect our global ad networks from billions in fraud and invalid activity, and to fiercely shield the advertiser trust at the very heart of Google’s platforms. We play an instrumental role in ensuring the long-term sustainability of the digital ads ecosystem, and ultimately, the free internet!

We are a diverse group of engineers, analysts, product & program managers, and researchers, collaborating cross-functionally to tackle complex, large-scale problems in the fight against invalid traffic (IVT). We work on some of the largest data sets in the world, build sophisticated detection systems, and apply state-of-the-art ML models. AI/Agent technologies are crucial in helping us scale our defenses and stay ahead of constantly evolving attacks.

## 1. Team's Background
arda atali

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


## 2. Why this team

I am interested as I see the chance to work on infrastructures that handles enormous data, and to apply AI to automate complex decision-making.

For trillions of events needed to be processing, the adversaries are constantly adapting, and the team is pushing agent-based approaches to stay ahead. 广告流量质量结合了所有这些——你要处理数万亿事件，对手不断适应，团队则在推动基于LLM的方法以保持领先。
Such combination is pretty exciting for me, as the problem evolves every day, and you never get to stop learning. 非常令人兴奋，因为问题每天都在变, 永远不会停止学习.

Sample follow-up: "What specifically interests you about fraud detection?"
*"I like that you can't just build a solution and walk away.*我喜欢你不能简单地构建解决方案然后离开——
*The attackers adapt, so engineers like us to keep evolving too. That feedback loop between detection and evasion is the kind of problem that keeps me engaged."*
攻击者会适应，所以工程技术也必须不断进化。这种侦测与规避之间的反馈循环正是让我保持投入的问题。


## 3. Questions for Arda

What does the balance between automated defenses and human review look like? 
What's the biggest technical challenge the team is facing right now? 

If question covered but not fully answered: 
*"You mentioned X earlier — that actually answers what I was going to ask about Y, but I'm also curious about..."*

### Question 1: AI/Agent

I'd love to hear more about how the team is using AI and agent technologies — 

For example, are there efforts to move towards more automatic agent workflows that can investigate new attack patterns on their own? 
我很想听听团队如何使用人工智能和代理技术——例如，是否有推动更自主的代理工作流程，能够自行调查新的攻击模式？

### Question 2: Detection-to-Defense Lifecycle: NEW attack type → production defense

From what I've read, the team both detects invalid traffic and builds automated defenses.团队既检测无效流量，还构建自动防御系统
During this process, systems operate with different latencies.系统运行延迟不一

Can you walk me through what that lifecycle looks like? 你能给我讲讲这个生命周期是怎样的吗？
For instance, when the team discovers a new type of attack, what does the path "from initial detection" to "a deployed, production defense" typically look like? 例如，当团队发现一种新型攻击时，从最初被发现到部署、生产防御的路径通常是什么样的？

### Question 3: Adversarial Feedback Loops

One thing interests me was the feedback loop. 
Let's say, when you deploy a new defense, sophisticated attackers could adapt and try to work around it. 部署新的防御时，成熟的攻击者可能会适应并试图绕过它

How does the team stay ahead of that cycle? 团队如何保持领先？
Is there a proactive ways to foresee new attack vectors, or is it more reactive? 预见新的攻击向量 or 隨機應變?

### Question 4: Onboarding

This domain sounds amazing - ad fraud, large-scale detection systems, the whole ads infrastructure stack. 

What does the ramp-up path look like for a new engineer joining the team? 
Are there specific areas where new people tend to start contributing first?
新工程师加入团队的晋升路径是怎样的？有没有哪些特定领域是新员工最先开始贡献的？

---