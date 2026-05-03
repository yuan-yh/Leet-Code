# Project
## OnCall Agent

OnCall Automation Agent | Spring Boot, RAG, ReAct, Multi-Agent, MCP	October 2025 - February 2026
•	Architected a multi-agent system that orchestrated Knowledge Index, ReAct chat, and Plan-Execute-Replan workflows to automate OnCall support. 
•	Built a RAG pipeline for internal docs, tuning chunking and Top-K retrieval to improve knowledge retrieval accuracy to 85%+.
•	Developed a ReAct chat agent with multi-turn memory and SSE streaming to support real-time Q&A, alert troubleshooting, and ticket preprocessing.
•	Integrated MCP tool calling with Prometheus, logs, MySQL, and web query tools, enabling agents to retrieve telemetry and execute external queries.
•	Implemented an AIOps planning agent that analyzes alerts, queries knowledge, and metrics, and generates remediation steps, reducing response time.

The team description explicitly calls out that "AI/Agent technologies are crucial in helping us scale our defenses." Your **OnCall Automation Agent** project is a direct proof point: you built a multi-agent system orchestrating RAG pipelines, ReAct chat agents, and Plan-Execute-Replan workflows. You also integrated MCP tool calling with Prometheus, logs, MySQL, and web query tools — essentially teaching an AI agent to pull telemetry and take action. This maps naturally to the team's use of LLMs and agent-based approaches to detect and respond to invalid traffic patterns.

**How to say it:** *"I noticed the team is increasingly leveraging AI and agent technologies — I saw the blog post about using LLMs for content review. I built an OnCall automation agent that orchestrates multiple AI workflows to analyze alerts, query knowledge bases and metrics, and generate remediation steps. The idea of applying that kind of agentic reasoning to fraud detection, where the system has to autonomously analyze patterns and decide how to respond, is exactly the kind of work I want to do."*
值班自动化代理 → AI/代理技术
团队描述明确指出，“人工智能/代理技术对于帮助我们扩展防御至关重要。”你的OnCall自动化代理项目是一个直接的证明：你构建了一个多代理系统，协调RAG管道、ReAct聊天代理以及规划-执行-重新规划工作流程。你还将MCP工具调用与Prometheus、日志、MySQL 和网页查询工具集成——本质上是在教AI代理拉取遥测数据并采取行动。这自然而然地与团队使用大型语言模型和基于代理的方法来检测和响应无效流量模式相呼应。
怎么说呢：“我注意到团队越来越多地利用人工智能和代理技术——我看到了一篇关于用大型语言模型进行内容审查的博客文章。我构建了一个OnCall自动化代理，协调多个AI工作流程，分析警报、查询知识库和指标，并生成修复步骤。将这种主体推理应用于欺诈检测，系统必须自主分析模式并决定如何应对，正是我想做的工作。”

### Project Introduction

**"Can you walk me through what the product was, what problem you were solving, and what your role and contributions were?"**
### Follow-ups
#### 1. Schema Design Trade-offs

优先事项1：多智能体架构（你最有力的话题）
这个项目有三位代理协作，而架构正是它令人印象深刻的地方：
核心见解是：不同的问题需要不同的推理模式。该项目使用两种不同的代理模式和一种基础设施代理：
（1） 知识库代理（RAG 流水线）——基础层。它会接收团队文档（警报手册、错误代码文档、API 规范），将其分块，通过阿里巴巴嵌入，并将向量存储在 Milvus 中。其他所有特工都依赖这些来获得有根据的答案。text-embedding-v4
（2） 聊天代理（ReAct模式）——用于开放式、交互式查询。当有人问“什么是错误代码12000001？”时，它会遵循“思考→行动→观察”循环：它推理该做什么，调用工具（例如日志查询、知识库检索），观察结果，并决定是否需要下一轮。这非常适合灵活且不可预测的问题。
（3） Ops Agent（计划-执行-重新计划模式）——用于结构化警报诊断。这是这个项目的主角。当警报触发（例如CPU满载）时，工作原理如下：
Alert arrives
    → Planner Agent: generates a multi-step investigation plan
        (Step 1: query error logs, Step 2: check process CPU ranking, Step 3: match knowledge base)
    → Executor Agent: executes step 1, returns results
    → Replanner Agent: evaluates results
        - If logs show nothing → replan (change keywords, expand time range)
        - If root cause found → terminate early, output report
        - Otherwise → proceed to next step
    → Loop until resolved or escalated to human
这对目标团队的重要性：这正是你用来检测和响应无效流量的模式——代理自主调查，当初始假设失败时调整，并生成结构化报告。“计划-执行-重新规划”循环是它与简单聊天机器人的区别。

优先事项2：工具与MCP集成（你的“教AI行动”故事）
这些代理不仅仅是在说话——他们会调用真实的系统。四个关键工具：
工具它的作用为什么重要query_prometheus_alerts从 Prometheus API 拉取活跃警报实时遥测摄取query_log（来源：腾讯云CLS MCP）自然语言→日志查询非工程师可以用纯语言查询日志get_current_time为LLM提供准确的时间戳解决了大型语言模型的“时间遗忘”问题query_internal_docs知识库上的向量相似性搜索真实文献中的理由
MCP角度很重要：MCP（模型上下文协议）就像AI工具的USB-C标准——任何按照MCP规范构建的工具都可以插入任何代理。日志查询工具使用腾讯云的 CLS MCP 服务器，代理发送自然语言（“显示过去一小时内ad_app的错误日志”），MCP 服务器会自动将其翻译成正确的查询语法。
值得了解的实现细节：Go 代码使用 Eino 框架（字节跳动的开源代理框架），将代理工作流建模为图——节点是原子能力（LLM、检索器、工具），边定义执行顺序和数据流。Java 版本使用 Spring-AI-Alibaba，并由 Supervisor Agent 协调 Planner + Executor 子代理。

优先事项3：RAG流水线（你的知识基础）
RAG流分为两个阶段：
离线（数据准备）：通过 Milvus →→存储嵌入→一级标题的文档块text-embedding-v4
在线（查询时间）：用户提问→嵌入→向量相似度搜索（余弦相似度，阈值0.8）→检索前三名→重新排序→给LLM，并严格要求提示
需要记住的关键设计决策：

0.8 相似阈值——故意提高，因为报警处理要求准确性而非回忆
团队采用语义标题而非固定代币计数的分块，使文档标准化，使每个标题涵盖一个完整的主题
反幻觉提示：“仅基于检索到的文件回答。如果你不知道，就说你不知道。”
反馈循环：用户可能会👎有错误的答案→日志ID被发送到团队聊天→手动审核→文档改进，→未来更好的答案


优先事项4：如何在面试中表达这个话题
团队简介写道：“人工智能/代理技术对于帮助我们扩大防御规模至关重要。”
你的叙述应该是：

“我构建了一个系统，让AI代理自主调查生产事件——从普罗米修斯提取遥测数据，通过自然语言查询日志，与已知问题的知识库匹配，并在初步假设未成立时动态调整调查计划。同一架构——多代理编排、针对监控系统的工具调用、基于RAG的决策——直接应用于大规模检测和响应无效流量模式。”

需要强调的关键类比点是：

自主调查→检测无效流量模式
规划-执行-重新规划→自适应响应工作流程
MCP工具集成→拉取遥测数据并在实时系统上执行操作
知识基础 + RAG →决策基于有文档的模式而非幻觉
每起事件→进行闭环学习，丰富了未来检测的知识基础


想让我更深入地探讨这些领域，还是根据项目文件中的面试问题做一个模拟问答流程会有帮助？你说：详细解释运营代理以及工具和MCP的集成。请更详细地解释运营代理以及工具与MCP的集成。
目标是帮助我在技术面试中自信地谈论这个项目做好准备。晚上7：25克劳德回答：让我给你详细讲解两者。Ops Agent 与工具集成的架构化全面解释Ops Agent 与工具集成的架构化全面解释让我给你详细讲解一下这两款游戏。我会把这段结构化，让你能内化每个作品的“为什么→什么→怎么做”——这才是面试中最有效的流程。

第一部分：行动特工——详细规划-执行-重新规划
为什么会出现这种模式
面试文档对此表述得非常好。传统待命有四个痛点：

没有结构化流程——初级工程师收到警报后，不知道是先检查日志还是先监控。他们会掉球。
当事情出错时无法适应——当日志显示没有异常时，人类就会卡住。他们僵住了。
数据孤岛——人类需要手动在Prometheus、日志平台、警报聊天组和内部文档之间切换。动作缓慢且容易出错。
知识存在于人们的脑海中——高级工程师知道“超时错误，先检查下游服务状态”。这种逻辑没有任何地方被规范。

简单的ReAct代理（思考-行动-观察循环）在这里不够用，因为ReAct是“边做边想”——没有预设计划，也没有结构化的进展跟踪。对于多步骤且步骤间有明显依赖关系的调查，你需要更有纪律性的东西。
三位副特工
可以把它想象成建筑师+承包商+项目经理：
规划器（规划器）——接收RAG的警报+相关文档，然后输出结构化的JSON计划：
JSON{
  "goal": "Investigate CPU 100% alert on server 10.0.1.5",
  "steps": [
    {
      "step_id": "1",
      "action": "query_log",
      "description": "Query error/warn logs from last 1 hour",
      "parameters": {"server": "10.0.1.5", "level": "error,warn", "time_range": "1h"},
      "expected_result": "Identify error patterns or process crashes"
    },
    {
      "step_id": "2",
      "action": "query_prometheus",
      "description": "Get process CPU ranking during spike window",
      "parameters": {"metric": "process_cpu", "time": "02:00-02:10"},
      "expected_result": "Identify which process is consuming CPU"
    },
    {
      "step_id": "3",
      "action": "query_internal_docs",
      "description": "Search knowledge base for this process's known CPU issues",
      "parameters": {"query": "{{step2_process_name}} CPU anomaly"},
      "expected_result": "Match against known resolution playbook"
    }
  ]
}
关键一点是：规划者不会执行任何事情。它只考虑需要哪些步骤以及按什么顺序进行。这种关注点的分离使系统可靠。
执行器（执行器）——仅取计划当前的第一步，调用相应工具，返回原始结果。这是故意“愚蠢”的——没有战略思考，只是准确地调用工具。这样可以隔离每个组件的故障模式。
重规划器（Replanner）——这里是智能所在。每次执行后，它会评估：
状况判决示例结果符合预期进入下一步日志显示错误→进入第二步context cancel结果是空的/意外的修改计划未发现错误日志→将关键词更改为 ，时间范围扩展为2小时"timeout OR cancel"提前达成目标终止在第2步确定根本原因→跳过第3步，输出报告无法继续升级需要跨团队沟通→人类旗帜
完整环形攻略（记住此示例）
这是文档中100%CPU的场景——这是你面试时的首选例子，因为它展示了适应能力：
第一轮：

规划工具生成三步计划（日志→流程排名→知识库）
执行者执行步骤1：查询错误/警告过去一小时的日志
结果：没有发现错误/警告日志，只有信息级别的cron job日志
Replanner 评估道：“没有错误意味着问题不是应用程序崩溃。重新优先级——先检查进程CPU排名。”
计划变异：第2步成为新的第1步，第2步变成了“专门为高CPU进程查询日志”

第二轮：

执行者运行新步骤1：02：00-02：10期间查询Prometheus进程CPU排名
结果：CPU使用率为95%（通常<10%）data-sync-service
Replanner评估道：“找到了罪魁祸首。计划依然有效，继续第二步。”

第三轮：

执行者执行步骤2：查询日志筛选到最后一小时data-sync-service
结果：“02：00触发了完全数据同步，迭代10M条记录，无分页”
Replanner评估道：“根本原因已确认。第三步（知识库查询）是不必要的——终止。”

最终成果：
Root cause: data-sync-service executed full data sync at 02:00 without pagination,
iterating 10M records causing CPU spike.
Recommendation: Add pagination (1000 records/batch), schedule during off-peak hours.
这个例子对你的面试很有说服力：它表明代理不仅仅是按剧本走——当第一步没有得到有用的信息时，他改变了计划。这种适应性正是调查初始信号可能误导的无效交通模式时所需要的。
它与ReAct的区别（请期待这个问题）
尺寸反应规划-执行-重新规划规划没有——一次只做一个决定完整计划先发布，按需修订最佳开放式问题，灵活探索多步骤任务，目标明确监督没有进展跟踪Replanner会跟踪每一步的结果风险可能会环绕或偏离赛道有结构化——更不容易浪费步骤你的项目聊天代理（临时回答问题、查询日志）Ops Agent（端到端诊断警报）
一句话：“当你事先不知道需要什么时，ReAct 很棒。“计划-执行-重新计划”适用于任务有足够结构、规划能带来回报——但当现实与计划不符时，你仍然需要灵活性。”

第二部分：工具与MCP深度集成
工具设计理念
项目的核心问题是：运维代理需要具备哪些能力来复制人类值班工程师的工作？
值班人员负责：查看警报→检查当前时间/持续时间→拉取日志→检查仪表盘→查阅内部文档→做出决策。所以代理需要一个工具来执行这些操作。
逐工具分析
（1） query_prometheus_alerts — 实时警报摄取

称普罗米修斯端点为/api/v1/alerts
从 JSON 中提取关键字段：警报名称、严重度、触发时间、受影响的服务、标签
这是行动特工的切入点——特工知道该调查什么

面试中提及时机：“代理从Prometheus中提取活跃警报，提取服务名称和时间窗口，这些作为后续日志和监控查询的参数。”
（2） get_current_time — 解决大型语言模型时间盲问题
这看似微不足道，但确实是一个值得一提的洞见。LLM不知道现在是什么时候。当客服需要计算“这个警报持续多久了？”或“过去一小时的查询日志”时，就需要一个准确的时间戳。
实现简洁——返回 Unix 时间戳（秒/毫秒/微秒）以及人类可读格式。输入/输出模式使用描述标签，使LLM能够理解每个字段的含义：jsonschema
走type GetCurrentTimeOutput struct {
    Seconds      int64  `json:"seconds" jsonschema:"description=Unix timestamp in seconds"`
    Milliseconds int64  `json:"milliseconds" jsonschema:"description=Unix timestamp in milliseconds"`
    Timestamp    string `json:"timestamp" jsonschema:"description=Human-readable format YYYY-MM-DD HH:MM:SS"`
}
何时提及：“即使是像时间感知这样简单的东西，也需要显式工具——大型语言模型没有'现在'的概念。这正是区分演示和制作系统的细节。”
（3） query_internal_docs — RAG驱动的知识检索

查询Milvus向量数据库
返回高于0.8余弦相似阈值的前3块
当LLM需要背景知识时（例如，“错误代码A是什么意思？”），自动触发。
通过将答案扎根于实际文件，防止幻觉

（4） query_log — 这是MCP集成工具。下面将详细介绍。
MCP：为什么重要以及它是如何运作的
打个比方（面试时用这个）：MCP就像AI工具的USB-C。键盘、显示器和外置硬盘都使用同一个USB-C接口。同样，MCP 定义了一个标准协议，使任何工具服务器都能插入任何代理客户端——每个工具无需自定义集成代码。
具体实现——日志查询工具：
该项目通过腾讯云CLS（云日志服务）的MCP服务器集成。流程如下：
User/Agent says: "Show me error logs from ad_app in the last 5 minutes"
         ↓
Agent forwards this natural language to CLS MCP Server
         ↓
MCP Server internally translates to proper CLS query syntax
         ↓
MCP Server executes query, returns structured log results
         ↓
Agent receives results, feeds to LLM for analysis
该代码创建了一个 SSE（服务器发送事件）MCP 客户端：
走// 1. Create SSE MCP client pointing to Tencent Cloud's MCP endpoint
cli, _ := client.NewSSEMCPClient("https://mcp-api.tencent-cloud.com/sse/ac4XXXXXX")
cli.Start(ctx)

// 2. Protocol negotiation (handshake)
initRequest := mcp.InitializeRequest{}
initRequest.Params.ProtocolVersion = mcp.LATEST_PROTOCOL_VERSION
cli.Initialize(ctx, initRequest)

// 3. Get all available tools from MCP server
mcpTools, _ := e_mcp.GetTools(ctx, &e_mcp.Config{Cli: cli})
之后，包含MCP服务器暴露的多种工具——项目文档显示CLS MCP提供了五个工具：mcpTools
MCP 工具目的GetCurrentTimestamp来自CLS服务器的时间戳GetRegionCodeByName将地区名称（“广州”）转换为代码GetTopicInfoByName查查日志主题/索引信息SearchLog执行结构化日志查询TextToSearchLogQuery自然语言→CLS查询语法
最后一个是关键能力——这意味着代理不需要知道 CLS 查询语法。它只是用通俗易懂的语言表达它想要的。
工具如何绑定到LLM
这点值得理解，因为面试官可能会问“函数调用到底是怎么工作的？”
走// 1. Collect all tools (MCP tools + custom tools)
toolList, _ := tools.GetLogMcpTool()           // MCP tools from CLS
toolList = append(toolList, NewGetCurrentTimeTool()) // Custom time tool

// 2. Extract tool schemas (name, description, parameters)
toolInfos := make([]*schema.ToolInfo, 0)
for _, t := range toolList {
    info, _ := t.Info(ctx)
    toolInfos = append(toolInfos, info)
}

// 3. Bind to the LLM — now the model knows what tools exist
chatModel.BindTools(toolInfos)
当LLM生成响应时，如果决定使用某个工具，API响应会包含一个包含工具名称和参数的字段，结构化JSON——无需字符串解析。这就是函数调用（与过去在系统提示中输入工具描述并希望LLM正确格式化响应的方式不同）。tool_calls
全套行动特工场景（把所有内容串联起来）
这里有一条服务中断警报，贯穿整个系统。请用这个作为你全面的面试示例：
1. TRIGGER: Prometheus fires "service_offline" alert

2. DATA COLLECTION:
   → query_prometheus_alerts → gets alert details (service name, trigger time)

3. TIME CALIBRATION:
   → get_current_time → calculates "alert has been active for 11 minutes"

4. LOG INVESTIGATION:
   → query_log (via CLS MCP) → "error logs from ad microservice, 
     5 minutes before service went offline"
   → MCP translates to CLS syntax, returns log snippets

5. KNOWLEDGE LOOKUP:
   → query_internal_docs → retrieves "service offline" playbook 
     from vector database

6. DECISION OUTPUT:
   → LLM synthesizes all data into structured report:
     - Log summary
     - Recommended steps from playbook  
     - Similar historical incidents
     - Whether human escalation is needed
第2至第5步均由计划-执行-重新计划循环协调，重新规划者在每步后评估是继续、调整还是终止。

适合采访的片段
这些建议放在你心里：
关于架构选择：“我选择了Plan-Execute-Replan而不是ReAct，因为警报调查本质上是一个结构化、多步骤的过程——但具体步骤需要根据每个工具的返回情况进行调整。纯脚本化的工作流程无法处理意外结果;纯ReAct代理会浪费步骤，没有计划。这种图案既给你结构感又灵活。”
关于MCP：“MCP标准化了代理调用外部工具的方式，就像USB-C标准化外设连接一样。实际好处是，同一日志查询工具可以在任何代理间重复使用，无需重写集成代码——而添加新数据源只是插入另一台MCP服务器。”
关于工具设计：“每个工具对应到人工值班工程师会采取的具体操作。代理的工作是按照正确的顺序和参数协调这些工具——这种编排逻辑是规划器和重新规划器负责的。”
关于对目标团队的相关性：“同样的架构适用于无效交通检测：代理提取遥测信号，将其与知识库中的已知模式进行核对，当初始信号不明确时调整调查方式，并自动生成可操作的报告——全部独立完成。”

想让我来个模拟问答环节，扮演面试官，探问你技术细节吗？