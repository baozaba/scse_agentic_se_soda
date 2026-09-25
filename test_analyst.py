"""Level 1 smoke test for the Analyst Agent.

Runs the real Analyst Agent end to end: reads the original brief.txt, sends it
to the agent, and lets the agent's own validation accept or reject its output.
The validated requirements are stored under artifacts/requirements.json and
displayed after the test ends.

The test fails (raises AssertionError) if the agent cannot turn the brief into
a usable requirements artifact.
"""

import json
import os

from analyst_agent import run_analyst

BRIEF_PATH = "brief.txt"
ARTIFACTS_DIR = "artifacts"
OUTPUT_PATH = os.path.join(ARTIFACTS_DIR, "requirements.json")


def read_brief(path=BRIEF_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    brief_text = read_brief()

    # Let the agent run as usual; its own validation accepts or rejects the
    # result (run_analyst returns None when validation failed).
    requirements = run_analyst(brief_text)
    assert requirements is not None, "Analyst Agent failed to produce requirements"

    # Store the validated artifact and display it.
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(requirements, f, indent=2)

    print(f"Saved validated requirements to {OUTPUT_PATH}:")
    print(json.dumps(requirements, indent=2))
    print("PASS: Analyst Agent smoke test passed")


if __name__ == "__main__":
    main()
