"""Level 2 behavioral test for the generated navigation logic.

Imports decide_next_move from the navigation logic artifact
(generated/navigation_logic.py) and calls it with known robot states, checking
that the returned action is valid and matches the expected move.

Each test case is a (label, state, expected_action) tuple.  `state` is the dict
the robot receives from its sensors:

    {
        "goal_ahead": bool,
        "goal_on_left": bool,
        "goal_on_right": bool,
        "front_blocked": bool,
        "left_blocked": bool,
        "right_blocked": bool,
    }

The expected action is one of "FORWARD", "LEFT", "RIGHT" or "STOP".
"""

import os
import sys

# Make generated/navigation_logic.py importable no matter where the test is
# launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generated.navigation_logic import decide_next_move

VALID_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}


def make_state(goal_ahead=False, goal_on_left=False, goal_on_right=False,
               front_blocked=False, left_blocked=False, right_blocked=False):
    """Build a sensor-state dict from its six boolean fields."""
    return {
        "goal_ahead": goal_ahead,
        "goal_on_left": goal_on_left,
        "goal_on_right": goal_on_right,
        "front_blocked": front_blocked,
        "left_blocked": left_blocked,
        "right_blocked": right_blocked,
    }


# A typical test case (the sample shared with us):
# {
#     "goal_ahead": True,  "goal_on_left": False, "goal_on_right": False,
#     "front_blocked": False, "left_blocked": False, "right_blocked": False
# }  ->  "FORWARD"
#
# Below, that sample is the first case, followed by the remaining robot states.
TEST_CASES = [
    # --- goal ahead ---
    ("goal ahead, all clear", make_state(goal_ahead=True), "FORWARD"),
    ("goal ahead, front blocked, sides clear", make_state(goal_ahead=True, front_blocked=True), "LEFT"),
    ("goal ahead, front and left blocked", make_state(goal_ahead=True, front_blocked=True, left_blocked=True), "RIGHT"),
    ("goal ahead, all blocked", make_state(goal_ahead=True, front_blocked=True, left_blocked=True, right_blocked=True), "STOP"),

    # --- goal on the left ---
    ("goal left, all clear", make_state(goal_on_left=True), "LEFT"),
    ("goal left, left blocked, front clear", make_state(goal_on_left=True, left_blocked=True), "FORWARD"),
    ("goal left, left and front blocked", make_state(goal_on_left=True, left_blocked=True, front_blocked=True), "RIGHT"),
    ("goal left, all blocked", make_state(goal_on_left=True, front_blocked=True, left_blocked=True, right_blocked=True), "STOP"),

    # --- goal on the right ---
    ("goal right, all clear", make_state(goal_on_right=True), "RIGHT"),
    ("goal right, right blocked, front clear", make_state(goal_on_right=True, right_blocked=True), "FORWARD"),
    ("goal right, right and front blocked", make_state(goal_on_right=True, right_blocked=True, front_blocked=True), "LEFT"),
    ("goal right, all blocked", make_state(goal_on_right=True, front_blocked=True, left_blocked=True, right_blocked=True), "STOP"),

    # --- no goal information ---
    ("no goal, all clear", make_state(), "FORWARD"),
    ("no goal, front blocked", make_state(front_blocked=True), "LEFT"),
    ("no goal, front and left blocked", make_state(front_blocked=True, left_blocked=True), "RIGHT"),
    ("no goal, all blocked", make_state(front_blocked=True, left_blocked=True, right_blocked=True), "STOP"),

    # --- ambiguous / unlikely states the logic may not handle as expected ---
    ("goals ahead and left, all clear", make_state(goal_ahead=True, goal_on_left=True), "FORWARD"),
    ("goals left and right, all clear", make_state(goal_on_left=True, goal_on_right=True), "LEFT"),
    ("goal ahead blocked, goal left clear", make_state(goal_ahead=True, goal_on_left=True, front_blocked=True), "LEFT"),
    ("goals ahead and left, both blocked", make_state(goal_ahead=True, goal_on_left=True, front_blocked=True, left_blocked=True), "RIGHT"),
]


def main():
    passed = 0
    failures = []

    for label, state, expected in TEST_CASES:
        result = decide_next_move(state)

        if result not in VALID_ACTIONS:
            failures.append((label, expected, result, "invalid action"))
            print(f"FAIL: {label}: expected {expected}, got {result!r} (not a valid action)")
        elif result != expected:
            failures.append((label, expected, result, "wrong move"))
            print(f"FAIL: {label}: expected {expected}, got {result}")
        else:
            passed += 1
            print(f"PASS: {label} -> {result}")

    total = len(TEST_CASES)
    print(f"\n{passed}/{total} behavioral test cases passed")

    if failures:
        print(f"{len(failures)} test case(s) failed")
        raise SystemExit(1)

    print("PASS: all behavioral test cases passed")


if __name__ == "__main__":
    main()
