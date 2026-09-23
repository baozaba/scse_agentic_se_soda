# SCSE 26 — Project: Agentic Software Engineering

Group: **Soda**

Engineer a simple robot-navigation system using three AI agents backed by
Qwen.  Each agent answers a different question, and each agent's validated
output becomes the next agent's input:

```
brief.txt ──► Analyst Agent ──► requirements.json ──► Planner Agent ──► plan.json ──► Developer Agent ──► navigation_logic.py
```

## The three agents

| Agent | Question it answers | Input artifact | Output artifact |
|-------|---------------------|----------------|-----------------|
| Analyst | *What* must the software achieve? | `brief.txt` | `artifacts/requirements.json` |
| Planner | *How* should the software behave? | `artifacts/requirements.json` | `artifacts/plan.json` |
| Developer | *What code* implements that behaviour? | `artifacts/plan.json` | `navigation_logic.py` |

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
- `run_developer.py` — reads `artifacts/plan.json`, writes `navigation_logic.py`.
- `navigation_logic.py` — the generated robot-navigation code.

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

## Running the full pipeline

Requires an Ollama server with the `qwen3:8b` model:

```bash
python brief_to_req.py     # -> robot_requirements.txt
python run_analyst.py      # -> artifacts/requirements.json
python run_planner.py      # -> artifacts/plan.json
python run_developer.py    # -> navigation_logic.py
```
