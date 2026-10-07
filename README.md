# Equity Research Agent — learn by building

Each stage is a self-contained folder that adds ONE new agent concept.
Run it, break it, read the code, then move on.

| Stage | Folder | Concept you learn | Output |
|---|---|---|---|
| 1 | `stage1_agent_loop/` | The agent loop: LLM + tools + loop. Tool schemas, `tool_use` / `tool_result` | Answers questions about a stock using live data |
| 2 | `stage2_research_workflow/` | Multi-step planning: fundamentals, valuation, news, risks -> structured report | Markdown research note per ticker |
| 3 | `stage3_rag_filings/` | RAG: chunk/embed 10-K/10-Q & earnings transcripts, cite sources | Answers grounded in filings, with citations |
| 4 | `stage4_analysis_tools/` | Deterministic tools: ratios, DCF, comps (code does the math, LLM interprets) | Valuation with explicit assumptions |
| 5 | `stage5_memory_and_multi_agent/` | Memory + specialist sub-agents (fundamental, news, risk) + orchestrator | Coordinated multi-agent report |
| 6 | `stage6_evals_and_guardrails/` | Evals, hallucination checks, number verification, tracing, cost control | Test suite + trustworthy outputs |
| 7 | `stage7_ship_it/` | Scheduling, watchlist alerts, simple UI/API | A usable product |

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Run Stage 1
```bash
python stage1_agent_loop/agent.py "Is AAPL expensive relative to its growth?"
```

> Educational project. Output is not investment advice.
