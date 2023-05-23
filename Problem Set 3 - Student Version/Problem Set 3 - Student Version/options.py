def question2_1():
    # 1. For question2_1, we want the policy to seek the near terminal state (reward +1) via the short
    # dangerous path (moving besides the row of -10 state).
    return {
        "noise": 0.002,
        "discount_factor": 0.1,
        "living_reward": -5.0
    }


def question2_2():
    # For question2_2, we want the policy to seek the near terminal state (reward +1) via the long safe path
    # (moving away from the row of -10 state).
    return {
        "noise": 0.2,
        "discount_factor": 0.3,
        "living_reward": -0.17
    }


def question2_3():
    # For question2_3, we want the policy to seek the far terminal state (reward +10) via the short
    # dangerous path (moving besides the row of -10 state).
    return {
        "noise": 0.1,
        "discount_factor": 0.9,
        "living_reward": -1
    }


def question2_4():
    # For question2_4, we want the policy to seek the far terminal state (reward +10) via the long safe path
    # (moving away from the row of -10 state).
    return {
        "noise": 0.2,
        "discount_factor": 0.99,
        "living_reward": 0.0
    }


def question2_5():
    # For question2_5, we want the policy to avoid any terminal state and keep the episode going on forever.
    return {
        "noise": 0.1,
        "discount_factor": 0.9,
        "living_reward": 5.0
    }


def question2_6():
    # For question2_6, we want the policy to seek any terminal state (even ones with the -10 penalty) and try to end the episode in the shortest time possible.
    return {
        "noise": 0.1,
        "discount_factor": 0.1,
        "living_reward": -12
    }
