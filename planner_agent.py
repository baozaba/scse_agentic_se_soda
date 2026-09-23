"""The Planner Agent.

The Analyst Agent decided *what* the software must achieve (the requirements).
The Planner Agent decides *how* the software should behave.

In a multi-agent system, the output of one agent becomes the context for the
next agent.  The Planner Agent therefore receives ONLY the validated
requirements produced by the Analyst Agent -- never the Analyst's raw
conversation (CONTEXT ISOLATION).  It turns those requirements into a
navigation plan, again as strict JSON produced by Qwen itself.
"""

import json

from ollama import chat

MODEL = "qwen3:8b"

# The exact keys the plan JSON contract allows -- nothing more, nothing less.
REQUIRED_KEYS = {"strategy", "decisions", "stop_condition"}

# ---------------------------------------------------------------------------
# The prompt: role, what the model must do, the constraints it must follow,
# and the final output structure.  This is what makes the agent deterministic.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a navigation planner for a mobile robot.\n"
    "You receive the validated software requirements produced by a "
    "requirements engineer.  Your job is to decide HOW the robot should "
    "behave in order to satisfy those requirements.\n\n"
    "You MUST reply with a single valid JSON object and nothing else "
    "(no markdown, no commentary, no surrounding text).\n\n"
    "The JSON object MUST contain exactly these three keys and no others:\n"
    "{\n"
    '    "strategy": "string",\n'
    '    "decisions": ["string", "string", ...],\n'
    '    "stop_condition": "string"\n'
    "}\n\n"
    "Rules you MUST follow:\n"
    '1. "strategy" is a single sentence describing the overall navigation '
    "strategy that satisfies the \"goal\".\n"
    '2. "decisions" is a list of the navigation decision rules the robot '
    "follows, each written as a short sentence.  Every rule must be phrased "
    "using ONLY the actions listed in \"allowed_actions\" and must respect "
    "\"safe_stop\" and \"avoid_obstacles\".  Do NOT invent any action that is "
    "not in \"allowed_actions\".\n"
    '3. "stop_condition" states the exact situation in which the robot must '
    "stop, in agreement with \"safe_stop\" and \"avoid_obstacles\".\n\n"
    "Example for allowed actions FORWARD, LEFT, RIGHT, STOP:\n"
    "{\n"
    '    "strategy": "Move toward the goal whenever that can be done safely, '
    "otherwise turn to an unblocked direction, and stop when none remain.\",\n"
    '    "decisions": [\n'
    '        "move FORWARD toward the goal when the path ahead is clear",\n'
    '        "turn LEFT or RIGHT when the goal direction is blocked",\n'
    '        "never move into a blocked direction",\n'
    '        "STOP when no safe direction is available"\n'
    "    ],\n"
    '    "stop_condition": "no safe direction is available"\n'
    "}\n\n"
    "Do not add any extra keys.  The output must be valid JSON."
)


def _call_qwen(messages):
    """Send a conversation to Qwen and return its raw text response."""
    response = chat(
        model=MODEL,
        messages=messages,
    )
    return response.message.content


def validate_plan(data):
    """Validate the plan produced by Qwen.

    Takes the result already converted into a Python data structure and checks
    that it is a valid dictionary containing exactly the required keys with the
    required types.  Prints a message and returns None on any violation.
    Returns the validated dictionary on success.
    """
    if not isinstance(data, dict):
        print("Error: expected a JSON object")
        return None

    keys = set(data.keys())
    if keys != REQUIRED_KEYS:
        missing = REQUIRED_KEYS - keys
        extra = keys - REQUIRED_KEYS
        print(f"Error: key mismatch, missing={sorted(missing)} extra={sorted(extra)}")
        return None

    if not isinstance(data["strategy"], str) or not data["strategy"].strip():
        print("Error: 'strategy' must be a non-empty string")
        return None

    if not isinstance(data["decisions"], list):
        print("Error: 'decisions' must be a list")
        return None

    if not data["decisions"]:
        print("Error: 'decisions' must not be empty")
        return None

    if not all(isinstance(decision, str) and decision.strip()
               for decision in data["decisions"]):
        print("Error: every decision must be a non-empty string")
        return None

    if not isinstance(data["stop_condition"], str) or not data["stop_condition"].strip():
        print("Error: 'stop_condition' must be a non-empty string")
        return None

    return data


def run_planner(requirement):
    """Turn the validated requirements into a validated navigation plan.

    - accepts the validated requirements (a dict) as a parameter,
    - sends the system prompt + requirements to Qwen,
    - accepts Qwen's response,
    - converts the JSON text into Python data (json.loads),
    - validates it,
    - returns the validated plan (or None if validation failed).
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(requirement)},
    ]

    raw = _call_qwen(messages)

    try:
        data = json.loads(raw)  # JSON text -> Python data
    except json.JSONDecodeError:
        print("Error: Qwen did not return valid JSON.")
        return None

    return validate_plan(data)
