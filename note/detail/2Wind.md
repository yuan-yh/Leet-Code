## Overview
• Improved PostgreSQL schemas by separating player profiles from season stats, simplifying cross-season queries and reducing redundant ingestion. 
• Built Python ingestion and backfill pipelines to migrate 16K+ player profiles and 72K+ game records from legacy APIs into Supabase/PostgreSQL. 
• Redesigned primary keys and upsert logic to eliminate duplicate records from repeated ingestion and support idempotent reruns. 
• Developed FastAPI endpoints for an AI coaching assistant, enabling agent-driven Q&A over player/team data through structured Supabase queries. 