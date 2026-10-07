"""Stage 1: the bare agent loop.

An agent is just:  while True: ask the model -> if it wants tools, run them -> feed results back.
No frameworks, so you can see every moving part.
"""
import json
import sys

import anthropic
import yfinance as yf

MODEL = "claude-sonnet-5-5"
MAX_STEPS = 8  # hard stop so a confused agent can't loop forever

SYSTEM = (
    "You are an equity research assistant. Use the tools to fetch data; never invent "
    "numbers. State which figures came from tools. End with a short, balanced view "
    "and note this is not investment advice."
)

# 1) Tool schemas: what the model is allowed to ask for.
TOOLS = [
    {
        "name": "get_quote",
        "description": "Current price, market cap, P/E, forward P/E, 52-week range for a ticker.",
        "input_schema": {
            "type": "object",
            "properties": {"ticker": {"type": "string", "description": "e.g. AAPL"}},
            "required": ["ticker"],
        },
    },
    {
        "name": "get_financials",
        "description": "Last 4 annual revenue, net income and operating cash flow for a ticker.",
        "input_schema": {
            "type": "object",
            "properties": {"ticker": {"type": "string"}},
            "required": ["ticker"],
        },
    },
]


# 2) Tool implementations: plain Python the model never sees, only its output.
def get_quote(ticker: str) -> dict:
    info = yf.Ticker(ticker).info
    keys = ["shortName", "currentPrice", "marketCap", "trailingPE", "forwardPE",
            "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "revenueGrowth", "profitMargins"]
    return {k: info.get(k) for k in keys}


def get_financials(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    inc, cf = t.income_stmt, t.cashflow
    out = {}
    for col in inc.columns[:4]:
        year = str(col.year)
        out[year] = {
            "revenue": _val(inc, "Total Revenue", col),
            "net_income": _val(inc, "Net Income", col),
            "operating_cash_flow": _val(cf, "Operating Cash Flow", col) if col in cf.columns else None,
        }
    return out


def _val(df, row, col):
    try:
        v = df.loc[row, col]
        return None if v != v else float(v)  # NaN -> None
    except KeyError:
        return None


REGISTRY = {"get_quote": get_quote, "get_financials": get_financials}


def run_tool(name: str, args: dict) -> str:
    try:
        return json.dumps(REGISTRY[name](**args), default=str)
    except Exception as e:  # return errors to the model so it can recover
        return json.dumps({"error": f"{type(e).__name__}: {e}"})


# 3) The loop.
def run_agent(question: str) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    for step in range(MAX_STEPS):
        resp = client.messages.create(
            model=MODEL, max_tokens=2000, system=SYSTEM, tools=TOOLS, messages=messages
        )
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":  # model is done
            return "".join(b.text for b in resp.content if b.type == "text")

        results = []
        for block in resp.content:
            if block.type == "tool_use":
                print(f"[step {step}] tool call: {block.name}({block.input})", file=sys.stderr)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input),
                })
        messages.append({"role": "user", "content": results})

    return "Stopped: hit MAX_STEPS without a final answer."


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Give me a quick fundamental snapshot of MSFT."
    print(run_agent(q))
