from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
import math
# TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state)

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.


def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[agent], None

    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action)
                           for index, (action, state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    turn = game.get_turn(state)  # to get the current player's turn

    # to check if the current state is terminal
    isTerminal, values = game.is_terminal(state)
    if isTerminal:
        # return the terminal value for the current player and None for the action
        return (values[turn], None)

    if max_depth == 0:  # Use max_depth to check if the search depth has been reached
        return (heuristic(game, state, 0), None)

    if turn == 0:  # Use turn to check if it is the max player's turn
        best_value = -math.inf  # initialize best value as negative infinity
        best_action = None

        # loop through list of possible actions from left of tree to right of tree
        for action in game.get_actions(state):
            next_state = game.get_successor(state, action)

            # Recursively call minimax on the next state
            result_value, _ = minimax(game, next_state, heuristic, max_depth-1)

            if result_value > best_value:  # check if result_value is greater than best_value
                best_value = result_value
                best_action = action

        return (best_value, best_action)

    else:  # then we are at min turn
        best_value = math.inf  # initialize best value as positive infinity
        best_action = None

        # loop through list of possible actions from left of tree to right of tree
        for action in game.get_actions(state):
            next_state = game.get_successor(state, action)

            # Recursively call minimax on the next state
            result_value, _ = minimax(game, next_state, heuristic, max_depth-1)

            if result_value < best_value:  # check if result_value is less than best_value
                best_value = result_value
                best_action = action

        return (best_value, best_action)

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.


def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction,
              max_depth: int = -1, alpha=-math.inf, beta=math.inf) -> Tuple[float, A]:

    # Get the current player's turn
    turn = game.get_turn(state)

    # Check if the current state is terminal
    isTerminal, values = game.is_terminal(state)
    if isTerminal:
        # Return the terminal value for the current player and None for the action
        return (values[turn], None)

    # Use max_depth to check if the search depth has been reached
    if max_depth == 0:
        return (heuristic(game, state, 0), None)

    if turn == 0:  # then we are at max turn
        best_value = -math.inf  # initialize best value as negative infinity
        best_action = None

        # Loop through list of possible actions from left to right of the tree
        for action in game.get_actions(state):
            next_state = game.get_successor(state, action)

            # Recursively call alphabeta on the next state with alpha and beta values
            result_value, _ = alphabeta(
                game, next_state, heuristic, max_depth-1, alpha, beta)

            # Check if result_value is greater than best_value
            if result_value > best_value:
                best_value = result_value
                best_action = action

            # Update alpha value to be the maximum of alpha and best_value
            alpha = max(alpha, best_value)

            # If alpha is greater than or equal to beta, prune remaining actions
            if alpha >= beta:
                break

        # Return the best value and best action found
        return (best_value, best_action)

    else:  # then we are at min turn
        best_value = math.inf  # initialize best value as positive infinity
        best_action = None

        # Loop through list of possible actions from left to right of the tree
        for action in game.get_actions(state):
            next_state = game.get_successor(state, action)

            # Recursively call alphabeta on the next state with alpha and beta values
            result_value, _ = alphabeta(
                game, next_state, heuristic, max_depth-1, alpha, beta)

            # Check if result_value is less than best_value
            if result_value < best_value:
                best_value = result_value
                best_action = action

            # Update beta value to be the minimum of beta and best_value
            beta = min(beta, best_value)

            # If alpha is greater than or equal to beta, prune remaining actions
            if alpha >= beta:
                break

        # Return the best value and best action found
        return (best_value, best_action)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action


def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha=-math.inf, beta=math.inf) -> Tuple[float, A]:
    # Get the current player's turn
    turn = game.get_turn(state)

    # Check if the current state is terminal
    isTerminal, values = game.is_terminal(state)
    if isTerminal:
        # Return the terminal value for the current player and None for the action
        return (values[0], None)

    # Use max_depth to check if the search depth has been reached
    if max_depth == 0:
        return (heuristic(game, state, 0), None)

    if turn == 0:  # then we are at max turn
        best_value = -math.inf  # initialize best value as negative infinity
        best_action = None
        descend_list = sorted([(heuristic(game, game.get_successor(state, action), 0), action)
                              for action in game.get_actions(state)], key=lambda x: x[0], reverse=True)
        # Loop through list of possible actions from left to right of the tree
        for _, action in descend_list:
            next_state = game.get_successor(state, action)

            # Recursively call alphabeta_with_move_ordering on the next state with alpha and beta values
            result_value, _ = alphabeta_with_move_ordering(
                game, next_state, heuristic, max_depth-1, alpha, beta)

            # Check if result_value is greater than best_value
            if result_value > best_value:
                best_value = result_value
                best_action = action

            # Update alpha value to be the maximum of alpha and best_value
            alpha = max(alpha, best_value)

            # If alpha is greater than or equal to beta, prune remaining actions
            if alpha >= beta:
                break

        # Return the best value and best action found
        return (best_value, best_action)

    else:  # then we are at min turn
        best_value = math.inf  # initialize best value as positive infinity
        best_action = None
        accend_list = sorted([(heuristic(game, game.get_successor(state, action), 0), action)
                             for action in game.get_actions(state)], key=lambda x: x[0])
        # Loop through list of possible actions from left to right of the tree
        for _, action in accend_list:
            next_state = game.get_successor(state, action)

            # Recursively call alphabeta_with_move_ordering on the next state with alpha and beta values
            result_value, _ = alphabeta_with_move_ordering(
                game, next_state, heuristic, max_depth-1, alpha, beta)

            # Check if result_value is less than best_value
            if result_value < best_value:
                best_value = result_value
                best_action = action

            # Update beta value to be the minimum of beta and best_value
            beta = min(beta, best_value)

            # If alpha is greater than or equal to beta, prune remaining actions
            if alpha >= beta:
                break

        # Return the best value and best action found
        return (best_value, best_action)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:

    # Get the current player's turn
    turn = game.get_turn(state)

    # Check if the current state is terminal
    isTerminal, values = game.is_terminal(state)
    if isTerminal:
        # Return the terminal value for the current player and None for the action
        return (values[0], None)

    # Use max_depth to check if the search depth has been reached
    if max_depth == 0:
        return (heuristic(game, state, 0), None)

    if turn == 0:  # then we are at max turn
        best_value = -math.inf  # initialize best value as negative infinity
        best_action = None

        # Loop through list of possible actions from left to right of the tree
        for action in game.get_actions(state):
            next_state = game.get_successor(state, action)

            # Recursively call expectimax on the next state with alpha and beta values
            result_value, _ = expectimax(
                game, next_state, heuristic, max_depth-1)

            # Check if result_value is greater than best_value
            if result_value > best_value:
                best_value = result_value
                best_action = action

        # Return the best value and best action found
        return (best_value, best_action)

    else:  # then we are at chance turn
        expected_value = 0  # initialize expected value as 0

        # Loop through list of possible actions from left to right of the tree
        action_count = 0
        for action in game.get_actions(state):
            next_state = game.get_successor(state, action)

            # Recursively call expectimax on the next state with alpha and beta values
            result_value, _ = expectimax(
                game, next_state, heuristic, max_depth-1)

            # Add the result_value to the expected_value
            expected_value += result_value

            action_count += 1

        # Calculate the average expected value
        expected_value /= action_count

        # Return the expected value and None for the action
        return (expected_value, None)
