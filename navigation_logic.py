def choose_action(blocked, goal_direction):
    if goal_direction is not None and not blocked[goal_direction]:
        return goal_direction
    for direction in ['FORWARD', 'LEFT', 'RIGHT']:
        if not blocked[direction]:
            return direction
    return 'STOP'
