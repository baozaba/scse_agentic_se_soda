"""Level 1 smoke test for the Planner Agent.

Runs the real Planner Agent end to end: reads the validated requirements from
artifacts/requirements.json, sends them to the agent, and lets the agent's own
validation accept or reject its output.  The validated plan is stored under
artifacts/plan.json and displayed after the test ends.

The test fails (raises AssertionError) if the agent cannot turn the
requirements into a plan the Developer Agent can use.
"""

import json
from pathlib import Path

from planner_agent import run_planner

REQUIREMENTS_PATH = Path("artifacts") / "requirements.json"
PLAN_PATH = Path("artifacts") / "plan.json"


def read_requirements(path=REQUIREMENTS_PATH):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    requirements = read_requirements()

    # Let the agent run as usual; its own validation accepts or rejects the
    # result (run_planner returns None when validation failed).
    plan = run_planner(requirements)
    assert plan is not None, "Planner Agent failed to produce a plan"

    # Store the validated artifact and display it.
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PLAN_PATH.open("w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    print(f"Saved validated plan to {PLAN_PATH}:")
    print(json.dumps(plan, indent=2))
    print("PASS: Planner Agent smoke test passed")


if __name__ == "__main__":
    main()
