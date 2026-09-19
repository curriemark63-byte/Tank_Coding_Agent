# Tank — Local Coding Agent

Tank is a local coding assistant running via Ollama on Qwen 2.5 Coder 7B, built and evaluated as part of a broader project exploring self-hosted LLMs for engineering and R&D work. This repo documents a structured evaluation of Tank's raw coding capability, and its growing autonomy in sourcing its own technical reference data, before wrapping it in full agent tooling.

## Setup

Tank is not yet wired into an agent framework (e.g. OpenClaw) — this repo currently documents Tank's raw coding capability, its live search infrastructure, and its progression toward self-sourced technical grounding, ahead of that step.

Tank runs locally via Ollama on Qwen 2.5 Coder 7B.

Interfaces via a custom chat script, `tank_chat.py`, with three modes:

* **code** — direct, runnable code output
* **teach** — conceptual explanations of the "why," not just the code
* **engineering** — electro-hydraulic servo valve topics (sensors, torque motors, flow/pressure characteristics, drift/anomaly detection) and data center engineering topics (thermal monitoring, cooling, power monitoring)

Tank also has live web search, via a dedicated local SearXNG instance (`tank_search.py`), used automatically when a query needs current documentation, datasheets, standards, or other technical information that shouldn't be pulled from training data alone.

## Round One: Baseline Coding Capability

Three tests, run as a progression of increasing complexity, with reference data and parameters supplied manually (sourced via Claude):

1. **Prime Number Check** — a quick baseline test of clean, direct code generation on a simple, self-contained problem
2. **Sensor Drift Simulation** — models long-term sensor drift (0.001 × full scale per year) as a random walk against a steady 500 PSI reading over a simulated year, plotted in a Jupyter notebook
3. **Anomaly Detection** — extends the drift simulation to flag and plot readings that deviate from true value by more than a threshold, and reports an anomaly count

**Findings:**

* **Explanation vs. code-only:** Tank's default behavior is to narrate how code works rather than output a clean code block, even when asked for "simple" code. An explicit instruction ("output only the code block") reliably fixes this.
* **Ambiguous phrasing sensitivity:** given "0.1% drift" as plain language, Tank computed the drift constant as 1% (10x too high) and repeated the identical mistake on a reworded retry. Spelling out the exact decimal (0.001) in the prompt resolved it.
* **Range vs. NumPy indexing bug:** Tank's first anomaly-detection attempt used Python's built-in `range()` for the time axis, which can't be boolean-indexed, causing a type error. Explicitly instructing it to use NumPy arrays throughout avoided the bug.

Tank passed all three tests, and consistently self-corrected once given more explicit instructions, suggesting the model's core coding logic is solid but benefits from very direct, unambiguous prompting rather than natural, loosely-worded requests.

## Round Two: Self-Sourced Technical Retrieval

With engineering mode's search pipeline in place, Round One's test structure was rerun — this time without supplying any reference data manually. Tank was given a plain-language engineering prompt and had to research the relevant background itself via live search before writing code.

1. **Sensor Drift Simulation** — Tank researched typical sensor drift models and independently wrote a `SensorDriftSimulator` class (bias drift, noise covariance, time-stepped simulation). Initially returned code with no plotting (only `numpy` imported); a follow-up prompt explicitly requesting a single complete runnable block, including matplotlib plotting, produced clean, working code with a plausible bias-drift curve.
2. **Anomaly Detection** — extending the same self-written drift model, Tank added a threshold-based flagging function and plotted anomalies directly on the drift curve. Flagged points lined up correctly with the drift spikes.
3. **Power Monitoring** — a new domain test (voltage/current simulation with a 150-watt threshold) to confirm the retrieval-and-code capability generalizes beyond servo/sensor topics. All readings above threshold were correctly flagged.

**Findings:**

* Tank's default response to an open-ended follow-up (e.g. "add plotting") was sometimes to ask clarifying questions or offer partial snippets rather than extend the existing code directly — resolved by re-prompting with a single, fully explicit, self-contained request rather than an incremental one.
* Once given a clean, complete prompt, Tank reliably retrieved relevant background and produced full, runnable code in one pass, across multiple engineering domains (sensor drift, anomaly detection, power monitoring).

**Takeaway:** Round One established that Tank's core coding logic is solid given explicit prompting. Round Two shows Tank can now independently source its own technical grounding — closing the gap between "coding assistant fed information" and "coding assistant that researches for itself" — a necessary step before layering on full agentic autonomy.

## Road Map

Agentic mode-switching (coder / teacher / engineer, chosen automatically rather than manually) via OpenClaw, along with safety guardrails: sandboxed execution, confirmation gates on destructive actions, file access scoped to the project directory, a command allow-list, and full audit logging.
