# Stage 1 exercises
1. Run it and watch the `[step N] tool call` lines on stderr. Does it call tools in parallel?
2. Ask about a fake ticker ("ZZZZ9"). How does the error flow back and how does the model react?
3. Add a `get_news(ticker)` tool (yfinance `Ticker.news`). You only edit TOOLS + REGISTRY.
4. Set MAX_STEPS=1 and observe the failure mode. Why do loop limits matter?
5. Remove "never invent numbers" from SYSTEM and compare answers. What changes?
