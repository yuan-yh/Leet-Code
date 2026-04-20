## Overview
1. Designed an AI-assisted breast cancer screening platform for underserved clinics to identify high-risk cases faster and generate structured reports. 
2. Built a multi-agent workflow with *FastAPI and LangGraph for VLM* analysis, retrieval, and case routing in mammogram and ultrasound review. 
3. Developed a modular *RAG* pipeline over medical literature with Qdrant hybrid retrieval and reranking to provide accurate clinical recommendations. 
4. Implemented JWT-authenticated APIs and *human-in-the-loop guardrails* to support secure review workflows with expert verification. 

```reference
• Independently designed and engineered a multimodal agentic system integrating domain-specific Vision-Language Models for breast cancer detection and 5-year risk prediction, processing mammograms, ultrasound images, histopathology slides, and EHR data to provide context-aware diagnostic support for clinical decision-making.
• Fine-tuned Gemma3-4B using a two-stage reinforcement learning pipeline: supervised fine-tuning (SFT) followed by Proximal Policy Optimization (PPO) with automatically evaluated symbolic rewards, enabling iterative diagnosis refinement through multi-turn natural dialogue.
• Integrated Mem0 dynamic memory framework with extraction and update phases for instantaneous memory updates, achieving faster, more accurate, cost-effective, and consistent long-term dynamic memory.
```


## General Questions
### Introduction
**Q1: "Walk me through the architecture of your breast cancer screening platform. How did the multi-agent workflow actually work?"**

Sure. So first a quick intro to give your the context:
    This platform was built for breast cancer screening centers in areas lack of experts, and the goal was to provide professional clinical guidance through a real-time voice conversation with our agent.

*The architecture has three main layers: VLM, RAG, and FastAPI.*

1. The VLM layer is a fined-tuned *Gemma3-4B*.

A two-stage RL pipeline (supervised fine-tuning then PPO) to analyze mammograms and ultrasounds and output BI-RADS scores (Breast Imaging Reporting and Data System) and structured findings. 

2. The retrieval layer was done with a RAG pipeline over about 300 medical documents using Qdrant.
Compared with the traditional RAG, we implemented a hybrid retrieval strategy, storing both dense and sparse vectors, then apply BGE-reranker to fetch the top 5 docs, sending into LLM.

> 用户提问 → 稠密向量检索 + 稀疏向量检索 → (Reciprocal Rank Fusion) RRF融合得到候选列表（top 30） → BGE-Reranker对这30个文档精排 → 取top K（5个）最相关的文档 → 送入LLM生成最终回答。

    This gave the agent grounded clinical context during the conversation, so its recommendations were backed by actual literature rather than just model knowledge.

3. And the backend was built in FastAPI to manage the agent workflow.
So image goes through VLM analysis, then retrieve medical literature, and then a voice-to-text-to-voice pipeline handles the real-time conversation. The agent reasons over the VLM output and retrieved context to provide clinical suggestions.

4. Safety guardrails 
At this moment, we also have the human-in-the-loop section like expert review and rating feedback to improve system quality.

For example, case where the model's confidence was low would get flagged and routed to remote specialists for review. 
Besides, every conversation ended with a rating piece for helpfulness and accuracy, which we used to iteratively improve this system.

    Model's LOW Confidence: VLM输出的softmax概率
    模型在做BI-RADS分级时，最后一层通常会输出各个类别的概率分布。比如模型判断某张钼靶为BI-RADS 4A，但概率只有0.35，而BI-RADS 3的概率是0.30——两个类别的概率非常接近，说明模型自己也"拿不准"。这时可以设定一个阈值规则，比如：如果最高概率低于**0.7**，或者前两个类别的概率差距小于0.15，就标记为低置信度。

### Data Security
**Q2: "How did you handle security and compliance for medical data?"**

*Authentication*: integrate Clerk with Google login to issue JWTs, and only authorized users can access the platform.

*Patient Data Storage*: screening and patient metadata were stored in Neon Postgres through Drizzle ORM. All communication ran over HTTPS.

No formal HIPAA compliance: as this was a research project at Northeastern, not a production clinical deployment. 

From my consideration, we'd like to have:
    - encryption for the databases and image storage, as well as the voice pipeline
    - more specific role-based access control, like separating general users/doctors, reviewer, and admin permissions
    - audit logging, on every access to patient data, 

    I would also be interested about how your company handles those security issues in the current architecture.

### RAG
**Q3: "Tell me about your RAG pipeline. How did you tune retrieval accuracy, and how did you know it was working?"**

The RAG pipeline could retrieve from about 300 medical documents, like clinical guidelines, imaging protocols, treatment literature. 

*Chunking*: 
First, we split by headings into sections.
Then for each section:
    Under *800* tokens: keep it as one chunk. 
    Over: split further at paragraph boundaries with *100*-token overlap to preserve context across chunks.

*Retrieval* / *Why Hybrid RAG*: 
We used hybrid search in Qdrant — so dense and sparse vectors together to improve terminology hit rate. 

While the team started with dense embeddings only, I noticed that it behaves less ideally on terminology-specific queries. 
For example, the BI-RADS subcategories (4A, 4B, 4C) - they are highly different in terms of clinical meanings, but their surrounding texts are similar, so embeddings for those chunks were nearly identical.
    Same problem with specific drug names — they'd get lost in the broader semantic space. 

In this case, adding sparse vectors (BM25-style keyword signals for exact match), then combining results to retrieve top 30 candidates - then top 5 for the LLM. 
This hybrid approach improved our hit rate on terminology-specific queries from around 70% to about 90%.

*Evaluation*: 
We built a test set of around 50 clinically realistic queries
    Like 'management of BI-RADS 4B lesions in dense breast tissue' or 'ultrasound features distinguishing fibroadenoma from phyllodes tumor.' 

For each query we checked whether at least one relevant chunk appeared in the top 5. Overall hit rate was 85 to 90%. We didn't have exhaustive relevance labels for formal recall measurement, but spot checks showed we were capturing the key guidelines.

*Failure*:
For the RAG part, we used to run into was mixed-topic chunks. 
A single chunk might contain both diagnostic criteria and follow-up scheduling. 
When that happened, the LLM would blend irrelevant content into its reasoning.
For example, when the user asks about diagnosis, the agent may talk about '6-month follow-up' which shouldn't be there. 

The fix was more granular splitting at the chunking stage.
And we also tried to tag topics in the metadata, like labeling each chunk as 'diagnosis,' 'treatment,' 'follow-up,'.
    So we could filter at retrieval time based on query intent.
    过滤太严格可能导致召回不足（比如某些跨主题的chunk本身确实有用但被过滤掉了），所以实际中通常的做法是：对过滤后的结果和不过滤的结果各取一部分，再合并送入reranker。这样兼顾了精准度和召回率。

### Failure / Decision
**Q4: "What was the hardest technical decision or failure you encountered on this project?"**

**Q5: "How did you handle edge cases or errors in the clinical workflow? What happened when the model got something wrong?"**

*Low-confidence VLM output*: 
When the model's confidence was low (like the softmax probability < 0.7) 
First, the agent should point it out: saying something like 'this finding suggests X, but I'd recommend specialist confirmation', rather than giving a definitive diagnosis. 
Second, the system auto-flagged the case and packaged the image, VLM output, and retrieved context together for remote expert review.

*RAG retrieval misses*: 
Be honest.
When no relevant chunks were found, the agent explicitly told the user: 'Our knowledge base doesn't have directly relevant guidelines for this question — I'd recommend consulting a specialist for further evaluation.' 

Behind the scenes, we logged that query as a knowledge gap.
Those missed queries would be reviewed to figure out whether 
    the gap was not covered — meaning we needed to add new documents
    or a retrieval failure from chunking or embedding quality, which meant we needed to tune the pipeline.

*Voice pipeline errors*: 
Vapi handles reconnection automatically if the connection drops. 

For the misheard clinical terms, the agent would summarize what it understood from the user before responding, giving the user a chance to catch errors. 

Users could also correct by typing manually if voice wasn't working well.

*Audit logging*: 
Every conversation was fully logged — the VLM output, retrieved chunks, and the full dialogue transcript. So when a conversation got a low rating, we could trace back through the entire pipeline to figure out where it went wrong: was it a bad VLM read, irrelevant retrieval, or the agent reasoning poorly over good inputs? That's how we closed the feedback loop.