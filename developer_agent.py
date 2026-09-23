"""The Developer Agent.

The Planner Agent decided *how* the robot should behave (the plan).  The
Developer Agent turns that plan into actual, runnable Python code.

It receives ONLY the validated plan produced by the Planner Agent -- not the
requirements, and not the Analyst's conversation (CONTEXT ISOLATION).  The
output is a complete Python module containing a navigation function, generated
by Qwen itself.
"""

import json

from ollama import chat

MODEL = "qwen3:8b"

# ---------------------------------------------------------------------------
# The prompt: role, what the model must do, the constraints it must follow,
# and the exact function it must produce.  This is what makes the agent
# deterministic.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a software developer for a mobile robot.\n"
    "You receive a validated navigation plan produced by a planner.  Your job "
    "is to turn that plan into runnable Python code.\n\n"
    "You MUST reply with Python code and nothing else: no markdown, no code "
    "fences, no commentary before or after the code.\n\n"
    "The code MUST define a function named choose_action with this exact "
    "signature:\n"
    "def choose_action(blocked, goal_direction):\n"
    "\n"
    "Where:\n"
    '  - blocked is a dict with keys "FORWARD", "LEFT", "RIGHT", each mapped '
    "to a boolean (True means that path is blocked).\n"
    '  - goal_direction is one of "FORWARD", "LEFT", "RIGHT" or None (None '
    "means the goal direction is unknown).\n"
    '  - the function returns exactly one of the strings "FORWARD", "LEFT", '
    '"RIGHT" or "STOP".\n\n'
    "The function MUST implement this exact algorithm:\n"
    "1. If goal_direction is not None and blocked[goal_direction] is False, "
    "return goal_direction.\n"
    "2. Otherwise, check FORWARD, LEFT and RIGHT in that order and return the "
    "first direction whose blocked value is False.\n"
    "3. If every direction is blocked, return STOP.\n\n"
    "The function MUST use the goal_direction parameter -- do NOT ignore it.\n\n"
    "The output must be valid Python."
)


def _call_qwen(messages):
    """Send a conversation to Qwen and return its raw text response."""
    response = chat(
        model=MODEL,
        messages=messages,
    )
    return response.message.content


def _strip_fences(text):
    """Remove markdown code fences if Qwen wrapped the code in them."""
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def validate_code(data):
    """Validate the Python code produced by Qwen.

    Takes the raw response text and checks that it is valid Python code that
    defines a function.  Prints a message and returns None on any violation.
    Returns the cleaned code string on success.
    """
    if not isinstance(data, str):
        print("Error: expected a string of Python code")
        return None

    code = _strip_fences(data.strip())
    if not code:
        print("Error: empty code")
        return None

    try:
        compile(code, "<qwen>", "exec")  # checks that the code is valid Python
    except SyntaxError as exc:
        print(f"Error: not valid Python ({exc})")
        return None

    if "def " not in code:
        print("Error: code must define a function")
        return None

    if "goal_direction" not in code:
        print("Error: code must use the goal_direction parameter")
        return None

    return code


def run_developer(plan):
    """Turn the validated plan into validated Python navigation code.

    - accepts the validated plan (a dict) as a parameter,
    - sends the system prompt + plan to Qwen,
    - accepts Qwen's response (raw text),
    - validates it,
    - returns the validated code string (or None if validation failed).
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(plan)},
    ]

    raw = _call_qwen(messages)

    return validate_code(raw)
