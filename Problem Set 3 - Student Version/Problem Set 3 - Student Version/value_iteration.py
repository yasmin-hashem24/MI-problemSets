from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent


class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A]  # The MDP used by this agent for training
    utilities: Dict[S, float]  # The computed utilities
    # The key is the string representation of the state and the value is the utility
    discount_factor: float  # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # We initialize all the utilities to be 0
        self.utilities = {state: 0 for state in self.mdp.get_states()}
        self.discount_factor = discount_factor

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        # If the state is terminal, its utility is 0
        if self.mdp.is_terminal(state):
            return 0
        # Find the action that maximizes the expected utility
        max_utility = float('-inf')
        for action in self.mdp.get_actions(state):
            expected_utility = 0
            # Compute the expected utility for each next state
            for next_state, probability in self.mdp.get_successor(state, action).items():
                # Compute the reward for transitioning to the next state
                reward = self.mdp.get_reward(state, action, next_state)
                # Compute the expected utility of the next state
                expected_utility += probability * \
                    (reward + self.discount_factor*self.utilities[next_state])
            # Update the maximum expected utility
            max_utility = max(max_utility, expected_utility)
        # Return the maximum expected utility
        return max_utility

    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        # Track the maximum utility change
        max_delta = 0
        # Create a new dictionary to store the updated utilities
        myutility = dict()
        # Compute the updated utility for each state
        for state in self.mdp.get_states():
            # Compute the old utility for the state
            old_utility = self.utilities[state]
            # Compute the new utility for the state using the Bellman equation
            new_utility = self.compute_bellman(state)
            # Store the new utility in the myutility dictionary
            myutility[state] = new_utility
            # Compute the absolute utility change for the state
            delta = abs(new_utility - old_utility)
            # Update the maximum utility change
            max_delta = max(max_delta, delta)
        # Update the agent's utility dictionary with the myutility dictionary
        self.utilities = myutility
        # Check if the maximum utility change is below the given tolerance
        if max_delta <= tolerance:
            # If so, return True to indicate that the utilities have converged
            return True
        # Otherwise, return False to indicate that the utilities have not converged
        return False

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        # Initialize the number of iterations to 0
        num_iterations = 0
        # Loop over the updates until either the desired number of iterations is reached or convergence is achieved
        while iterations is None or num_iterations < iterations:
            # Increment the number of iterations
            num_iterations += 1
            # Call the update function to update the utilities of the states
            # If the update function returns True, then the utilities have converged and we can stop iterating
            if self.update(tolerance):
                break
        # Return the number of iterations that were performed
        return num_iterations

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        # Check if the state is terminal
        if self.mdp.is_terminal(state):
            # If so, return None to indicate that no action can be taken
            return None
        # Initialize the best action and best utility to None and negative infinity, respectively
        best_action = None
        best_utility = float('-inf')
        # Loop over all possible actions for the state
        for action in env.actions():
            # Compute the expected utility of taking the action in the state
            expected_utility = 0
            # Loop over all possible next states and their probabilities
            for next_state, probability in self.mdp.get_successor(state, action).items():
                # Compute the expected utility of transitioning to the next state
                expected_utility += probability * \
                    (self.mdp.get_reward(state, action, next_state) +
                     self.discount_factor*self.utilities[next_state])
            # Check if the expected utility of the current action is better than the current best utility
            if expected_utility > best_utility:
                # If so, update the best action and best utility accordingly
                best_action = action
                best_utility = expected_utility
        # Return the best action for the state
        return best_action

    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(
                state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)

    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(
                state): value for state, value in utilities.items()}
