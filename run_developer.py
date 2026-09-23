"""Runner: read the validated plan, run the Developer Agent, and save the
generated Python code as navigation_logic.py.
"""

import json
from pathlib import Path

from developer_agent import run_developer

PLAN_PATH = Path("artifacts") / "plan.json"
OUTPUT_PATH = Path("navigation_logic.py")


def read_plan(path=PLAN_PATH):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    plan = read_plan()

    # Call the agent and receive the final validated navigation code.
    code = run_developer(plan)

    # Store the generated code in navigation_logic.py.
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write(code + "\n")

    print(f"Saved generated code to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
