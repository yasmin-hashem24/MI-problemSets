from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment


@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body
    # where the head is the first point and the tail is the last
    direction: Direction    # The direction that the snake is moving towards
    # The location of the apple. If the game was already won, apple will be None
    apple: Optional[Point]


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y)
                           for x in range(self.width)
                           for y in range(self.height)
                           if Point(x, y) not in snake_positions
                           ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            # Initialize the random generator using the seed
            self.rng.seed(seed)
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        center_x = self.width // 2
        center_y = self.height // 2
        self.snake = [Point(center_x, center_y)]
        self.direction = Direction.LEFT

        # Generate the first apple
        self.apple = self.generate_random_apple()

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # TODO add your code here
        # a snake can wrap around the grid
        # NOTE: The action order does not matter
        # The snake can wrap around the grid

        # snake can only move into the orthogonal directions to it's current or keep going as in none
        currentDirection = self.direction
        if currentDirection == Direction.LEFT:
            return [Direction.DOWN, Direction.UP, Direction.NONE]
        elif currentDirection == Direction.RIGHT:
            return [Direction.UP, Direction.DOWN, Direction.NONE]
        elif currentDirection == Direction.UP:
            return [Direction.RIGHT, Direction.LEFT, Direction.NONE]
        elif currentDirection == Direction.RIGHT:
            return [Direction.UP, Direction.DOWN, Direction.NONE]

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # TODO Complete the following function
        done = False
        reward = 0
        head = self.snake[0]
        if action != Direction.NONE:
            new_head = head + Direction.to_vector(action)
        else:
            new_head = head + self.direction.to_vector()
        # Check if the new head position is outside the grid
        if new_head.x < 0:
            new_head = Point(self.width - 1, new_head.y)
        elif new_head.x >= self.width:
            new_head = Point(0, new_head.y)
        elif new_head.y < 0:
            new_head = Point(new_head.x, self.height - 1)
        elif new_head.y >= self.height:
            new_head = Point(new_head.x, 0)

       # Check if the new head overlaps with the snake body and is not the tail
        if new_head in self.snake[1:-1]:
            done = True
            reward = -100

            observation = SnakeObservation(
                tuple(self.snake), self.direction, self.apple)

            return observation, reward, done, {}

        # Check if the new head overlaps with the apple
        if new_head == self.apple:
            # Grow the snake by adding the new head
            self.snake.insert(0, new_head)
            # Generate a new apple in a free cell
            self.apple = self.generate_random_apple()
            # Increase the reward by 1 for eating an apple
            reward = 1
        else:
            # Move the snake by adding the new head and removing the tail
            self.snake.pop()
            self.snake.insert(0, new_head)
            # No reward for moving the snake without eating an apple
            reward = 0

        # Check if the snake covers all the cells in the grid
        if len(self.snake) == self.width * self.height:
            done = True
            reward = 100

        observation = SnakeObservation(
            tuple(self.snake), self.direction, self.apple)

        return observation, reward, done, {}

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake),
            self.parse_action(direction),
            Point(*apple)
        )

    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))

    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]

    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]
