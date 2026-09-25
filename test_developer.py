"""Level 1 smoke test for the Developer Agent.

Runs the real Developer Agent end to end: reads the validated plan from
artifacts/plan.json, sends it to the agent, and lets the agent's own
validation accept or reject its output.  The generated code is stored under
generated/navigation_logic.py and displayed after the test ends.

The test fails (raises AssertionError) if the agent cannot turn the plan into
a Python module that defines decide_next_move(state).
"""

import json
from pathlib import Path

from developer_agent import run_developer

PLAN_PATH = Path("artifacts") / "plan.json"
OUTPUT_PATH = Path("generated") / "navigation_logic.py"


def read_plan(path=PLAN_PATH):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    plan = read_plan()

    # Let the agent run as usual; its own validation accepts or rejects the
    # result (run_developer returns None when validation failed).
    code = run_developer(plan)
    assert code is not None, "Developer Agent failed to produce navigation code"

    # Store the generated code and display it.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write(code + "\n")

    print(f"Saved generated code to {OUTPUT_PATH}:")
    print(code)
    print("PASS: Developer Agent smoke test passed")


if __name__ == "__main__":
    main()
