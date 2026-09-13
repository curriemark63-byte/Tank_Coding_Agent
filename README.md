# Tank — Local Coding Agent

Tank is a local coding assistant running via Ollama on Qwen 2.5 Coder 7B, 
built and evaluated as part of a broader project exploring self-hosted LLMs 
for engineering and R&D work. This repo documents a structured evaluation 
of Tank's raw coding capability before wrapping it in agent tooling.
## Setup

Tank is not yet wired into an agent framework (e.g. OpenClaude) — this repo currently documents Tank's raw coding capability, plus its supporting search infrastructure, ahead of that step.

Tank runs locally via Ollama on Qwen 2.5 Coder 7B.

Interfaces via a custom chat script, `tank_chat.py`, with three modes:
- **code** — direct, runnable code output
- **teach** — conceptual explanations of the "why," not just the code
- **engineering** — electro-hydraulic servo valve topics (sensors, torque motors, flow/pressure characteristics, drift/anomaly detection) and data center engineering topics (thermal monitoring, cooling, power monitoring)

Tank also has live web search, via a dedicated local SearXNG instance (`tank_search.py`), used automatically when a query needs current documentation, datasheets, standards, or other technical information that shouldn't be pulled from training data alone.

## Test Methodology

Three tests, run as a progression of increasing complexity:

1. **Prime Number Check** — a quick baseline test of clean, direct code 
   generation on a simple, self-contained problem
2. **Sensor Drift Simulation** — models long-term sensor drift (0.001 × full 
   scale per year) as a random walk against a steady 500 PSI reading over a 
   simulated year, plotted in a Jupyter notebook
3. **Anomaly Detection** — extends the drift simulation to flag and plot 
   readings that deviate from true value by more than a threshold, and 
   reports an anomaly count

## Findings

- **Explanation vs. code-only**: Tank's default behavior is to narrate how 
  code works rather than output a clean code block, even when asked for 
  "simple" code. An explicit instruction ("output only the code block") 
  reliably fixes this.
- **Ambiguous phrasing sensitivity**: given "0.1% drift" as plain language, 
  Tank computed the drift constant as 1% (10x too high) and repeated the 
  identical mistake on a reworded retry. Spelling out the exact decimal 
  (0.001) in the prompt resolved it.
- **Range vs. NumPy indexing bug**: Tank's first anomaly-detection attempt 
  used Python's built-in `range()` for the time axis, which can't be 
  boolean-indexed, causing a type error. Explicitly instructing it to use 
  NumPy arrays throughout avoided the bug.

## Takeaway

Tank passed all three tests, and consistently self-corrected once given 
more explicit instructions, suggesting the model's core coding logic is 
solid but benefits from very direct, unambiguous prompting rather than 
natural, loosely-worded requests. This will inform how Tank's system 
prompt and any future fine-tuning are approached before it's built out 
into a full coding agent.

## Road map 

Agentic capabilities soon.
