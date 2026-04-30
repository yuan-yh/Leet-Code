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