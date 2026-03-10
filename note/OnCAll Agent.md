# 智能 OnCall Agent

一个面向运维值班场景的 AI 自动化助手。它的核心目标是帮值班工程师处理那些高频、重复的告警和故障，让工程师把精力留给真正复杂的问题。

Reference: https://my.feishu.cn/wiki/K6dtwsCbSiKme9kk01BctRbBnJe

## Core Functions:

### 1. 文档上传知识库 (知识库 Agent - RAG)

团队可以把故障处理手册、服务接入说明等文档上传到系统。系统通过知识库 Agent 对文档做 Embedding 并存储，为后续的智能问答和诊断提供知识基础。

Why RAG: 

- 如果把大量文档（故障手册、服务说明等）全部塞进大模型的上下文窗口，会有三个问题: 成本高、速度慢、准确率低。

- 所以知识库 Agent 采用"先检索、再生成"的策略，只把最相关的片段喂给模型，既省 token 又提高回答质量。

### 2. 对话式查询 (对话 Agent - HTTP & SSE)

值班人员可以用自然语言直接问系统问题，比如"错误码 12000001 是什么原因？"系统会从知识库中召回相关内容，结合历史对话上下文，给出精准回答。支持**快速对话（HTTP 一次性返回）和流式对话（SSE 逐步输出）**两种模式。

### 3. AIOps 自动诊断 (运维 Agent)

当系统收到告警通知（比如接口失败率过高）后，运维 Agent 会自动启动一个多步骤的诊断流程：

- 先由 Planner Agent 规划排查步骤，

- 再由 Executer Agent 执行（比如调用日志 API 查 error 日志、拉取监控面板看趋势），

- 如果中途需要调整计划，Replanner Agent 会重新规划。

- 最后还会把本次处理的经验更新回知识库，闭环沉淀  ，让系统越用越聪明。

## 整体架构：四层结构**分层解耦**

```
┌─────────────────────────────────────────┐
│           接入层 (API Layer)              │
│  /chat  /chat_stream  /upload_file  /ai_ops │
└──────────────┬──────────────────────────┘
               ↑
┌──────────────┴──────────────────────────┐
│           业务层 (Agent Layer)            │
│    对话Agent  运维Agent  知识库Agent       │
└──────────────┬──────────────────────────┘
               ↑
┌──────────────┴──────────────────────────┐
│         服务层 (核心组件层)               │
│  Loader / Indexer / Retriever / Transformer │
│  Chat Model / Prompt / Tool / MCP        │
└──────────────┬──────────────────────────┘
               ↑
┌──────────────┴──────────────────────────┐
│         存储层 (知识库)                   │
│  各类手册、工单文档 → Vector Database     │
└─────────────────────────────────────────┘
```

1. 接入层: 对外暴露4个API接口，只负责接收请求、转发给业务层。

| 接口 | 用途 |
|---|---|
| `/chat` | 普通对话（同步返回） |
| `/chat_stream` | 流式对话（SSE实时推送） |
| `/upload_file` | 上传文档到知识库 |
| `/ai_ops` | 触发运维诊断 |

2. 业务层: 向接入层提供可用的Agent (知识库/对话/运维Agent)

3. 服务层 (核心组件): 提供Agent调用的组件, 组件层可以被多个Agent复用

数据处理组：知识库Agent, 让文档变成可检索的知识
Loader      → 读取文件（PDF/Word/Markdown等）
Indexer     → 分片 + Embedding + 存入向量库
Retriever   → 召回 + 重排序
Transformer → 格式转换（比如把表格转成文本）

AI推理组：让LLM能被标准化调用, 所有Agent共用
Chat Model  → 封装LLM调用（换模型只改这里）
Prompt      → 管理所有提示词模板

能力扩展组：让Agent能与外部世界交互
Tool   → 内部工具（查日志、查监控、发消息等）
MCP    → 外部系统调用（标准化协议）

4. 存储层: 所有文档存入 Vector Database（向量数据库），支持语义相似度检索。

Example of File Upload API:

接入层  FileUploadController   ← Controller (只负责接收请求和返回响应，不写任何业务逻辑，业务全部委托给Service层)
           ↓ 调用
业务层  VectorIndexService     ← indexSingleFile()
           ↓ 调用
服务层  ChunkService           ← 分片
        EmbeddingService       ← 向量化
        MilvusClient           ← 存储

### Agent的核心设计模式

#### 知识库Agent

> 核心模式：RAG模式（检索增强生成）

##### 1. 上传时：文档 → 分片 → (索引) Embedding → 存入向量库 (存储的是 向量+原始文本 两份数据)

- 文件分块 (两层分片策略)

第一层：按Markdown标题(#)切分成多个Section

第二层：对每个Section判断大小
  ├── Section < MaxSize (800)  → 直接作为一个分片
  └── Section > MaxSize (800)  → 按段落边界继续切分
                                + Overlap重叠（100, 相邻分片之间有内容重叠, 保留上下文语义连贯）

- 索引（向量化+存储）

第一步：向量化 (Embedding), 调用阿里云DashScope API

第二步：构建元数据 (路径, 第几个分片, 总分片数, 章节标题)

第三步：存入Milvus (UUID, 原始文本片段, vector, 元数据)

- 整体流程串联

读文件
  → 按标题分Section
    → 每个Section判断大小 → 按段落切分+Overlap保持上下文, MaxSize=800
      → 每个chunk：
        调用DashScope API → 生成vector
        构建metadata（路径、索引等）
        存入Milvus：{ content (最终喂给LLM), vector, metadata }

##### 2. 查询时：问题向量化 → 召回 (查top10最相似的片段) → 重排 (計算语义相似度) → 生成答案 (top3片段原始文本+问题 -> LLM回答)

> 召回（Top 10）和重排（Top 3）用的是**不同的模型**

- 召回部分用的是 Milvus内置的L2距离搜索: `java.withMetricType(io.milvus.param.MetricType.L2)  // 欧式距离`

召回  → Embedding模型 + 向量相似度算法（余弦相似度）
        速度快、成本低，但准确率有限

重排  → Cross Encoder模型
        逐对计算语义相关性，慢但准确率高
```

#### 对话Agent

- 核心模式：RAG召回 (獲取context構建system prompt) + ReAct (Reasoning + Act工具调用)多輪交互
- 思考 (查什麽) → 行动 (用工具) → 观察，循环直到有答案

#### 运维Agent

- 核心模式：RAG召回 (獲取context + tool info構建system prompt) + Plan → Execute → Replan （规划→执行→调整）多輪交互
- Planner制定排查计划 → Executor调用工具执行 → Replanner评估并调整

ReAct VS Plan-Execute-Replan
- ReAct 每步只想一步，走一步看一步; Plan-Execute-Replan先想清楚全部步骤，再逐步执行。两者本质相似，差别在于是否需要全局计划。
