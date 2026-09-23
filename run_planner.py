"""Runner: read the validated requirements, run the Planner Agent, and save
the validated navigation plan as artifacts/plan.json.
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

    # Call the agent and receive the final validated navigation plan.
    plan = run_planner(requirements)

    # Save it as JSON inside the artifacts folder.
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PLAN_PATH.open("w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    print(f"Saved validated plan to {PLAN_PATH}:")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
