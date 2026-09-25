# SCSE 26 — Project: Agentic Software Engineering

Group: **Soda**

Engineer a simple robot-navigation system using three AI agents backed by
Qwen.  Each agent answers a different question, and each agent's validated
output becomes the next agent's input:

```
brief.txt ──► Analyst Agent ──► requirements.json ──► Planner Agent ──► plan.json ──► Developer Agent ──► generated/navigation_logic.py
```

## The three agents

| Agent | Question it answers | Input artifact | Output artifact |
|-------|---------------------|----------------|-----------------|
| Analyst | *What* must the software achieve? | `brief.txt` | `artifacts/requirements.json` |
| Planner | *How* should the software behave? | `artifacts/requirements.json` | `artifacts/plan.json` |
| Developer | *What code* implements that behaviour? | `artifacts/plan.json` | `generated/navigation_logic.py` |

Each agent only receives the previous agent's validated artifact — never the
previous agent's full conversation (**context isolation**).

## Files

- `brief.txt` — the customer's robot-navigation brief (human language).
- `brief_to_req.py` — exercise: ask Qwen for free-form requirements, run it
  several times to show the output is *not* consistent.
- `analyst_agent.py` — the Analyst Agent (`run_analyst`, `validate_requirements`).
- `run_analyst.py` — reads `brief.txt`, writes `artifacts/requirements.json`.
- `planner_agent.py` — the Planner Agent (`run_planner`, `validate_plan`).
- `run_planner.py` — reads `artifacts/requirements.json`, writes `artifacts/plan.json`.
- `developer_agent.py` — the Developer Agent (`run_developer`, `validate_code`).
- `run_developer.py` — reads `artifacts/plan.json`, writes `generated/navigation_logic.py`.
- `generated/navigation_logic.py` — the generated robot-navigation code, exposing
  `decide_next_move(state)` (the single entry point other programs call).
- `test_analyst.py` — Level 1 smoke test for the Analyst Agent.
- `test_planner.py` — Level 1 smoke test for the Planner Agent.
- `test_developer.py` — Level 1 smoke test for the Developer Agent.
- `test_generated_navigation_logic.py` — Level 2 behavioral test for
  `decide_next_move(state)`.

## Requirements JSON contract

```json
{
  "goal": "string",
  "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
  "safe_stop": true,
  "avoid_obstacles": true
}
```

## Plan JSON contract

```json
{
  "strategy": "string",
  "decisions": ["string", "string", "..."],
  "stop_condition": "string"
}
```

## Testing

Two levels of tests cover the pipeline:

- **Level 1 — Agent / pipeline smoke tests.** Run the real agents with their
  real inputs and let each agent's own validation accept or reject its output:

  ```bash
  python test_analyst.py    # brief.txt         -> artifacts/requirements.json
  python test_planner.py    # requirements.json -> artifacts/plan.json
  python test_developer.py  # plan.json         -> generated/navigation_logic.py
  ```

- **Level 2 — Behavioral testing.** Call `decide_next_move(state)` with known
  sensor states and check the returned action:

  ```bash
  python test_generated_navigation_logic.py
  ```

## Running the full pipeline

Requires an Ollama server with the `qwen3:8b` model:

```bash
python brief_to_req.py     # -> robot_requirements.txt
python run_analyst.py      # -> artifacts/requirements.json
python run_planner.py      # -> artifacts/plan.json
python run_developer.py    # -> generated/navigation_logic.py
```
