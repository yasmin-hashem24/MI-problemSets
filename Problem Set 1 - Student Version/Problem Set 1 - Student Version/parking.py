from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem


class ParkingProblem(Problem[ParkingState, ParkingAction]):
    # A set of points which indicate where a car can be (in other words, every position except walls).
    passages: Set[Point]
    # A tuple of points where state[i] is the position of car 'i'.
    cars: Tuple[Point]
    # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
    slots: Dict[Point, int]
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.
   # dicitionary of cost values of getting in another car's slot
    values: Dict[str, int] = {'A': 26, 'B': 25, 'C': 24, 'D': 23, 'E': 22, 'F': 21,
                              'G': 20, 'H': 19, 'I': 18, 'J': 17, 'K': 16, 'L': 16, 'M': 15, 'N': 14, 'O': 13}

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        return self.cars

        # This function should return True if the given state is a goal. Otherwise, it should return False.

    def is_goal(self, state: ParkingState) -> bool:
        # TODO: ADD YOUR CODE HERE
        # checking on the x and y corrinates of the state tuple if it matches the requriedgoal
        # it not in any then not the state
        for slot in self.slots.keys():
            if slot.x != state[self.slots[slot]].x or slot.y != state[self.slots[slot]].y:
                return False

        return True

        # This function returns a list of all the possible actions that can be applied to the given state

    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # TODO: ADD YOUR CODE HERE

     # listing down the possible moves according to the action class in point format for addition
        rightmove = Point(1, 0)
        lefttmove = Point(-1, 0)
        upmove = Point(0, -1)
        downmove = Point(0, 1)

      # creating variables for the new possible positions
        newrightpos = None
        newleftpos = None
        newuppos = None
        newdownpos = None

        actions = []
        for i, car in enumerate(state):
            # i is the index of the car and car is the position i point format to loop over
            # itnializing the possible new psotions
            newrightpos = car+rightmove
            newleftpos = car+lefttmove
            newuppos = car+upmove
            newdownpos = car+downmove
            # if the new right psotiion is not a wall and not another car slot-> add it to the possible actions
            if newrightpos in self.passages and newrightpos not in state:
                actions.append((i, Direction.RIGHT))
            # if the new left psotiion is not a wall and not another car slot-> add it to the possible actions
            if newleftpos in self.passages and newleftpos not in state:
                actions.append((i, Direction.LEFT))
              # if the new up psotiion is not a wall and not another car slot-> add it to the possible actions
            if newuppos in self.passages and newuppos not in state:
                actions.append((i, Direction.UP))
             # if the new down psotiion is not a wall and not another car slot-> add it to the possible actions
            if newdownpos in self.passages and newdownpos not in state:
                actions.append((i, Direction.DOWN))

        return actions

        # This function returns a new state which is the result of applying the given action to the given state

    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        newstate = None
        index, dir = action  # intialize the index of the car and action direction
        new_state = list(state)  # the new possible state of the car
        rightmove = Point(1, 0)  # the possible moves
        lefttmove = Point(-1, 0)
        upmove = Point(0, -1)
        downmove = Point(0, 1)
        if dir == Direction.DOWN:  # check the direction of movmenet pre intialized to pick which possiblemove is the new state going to be
            newstate = state[index]+downmove
        if dir == Direction.UP:
            newstate = state[index]+upmove
        if dir == Direction.RIGHT:
            newstate = state[index]+rightmove
        if dir == Direction.LEFT:
            newstate = state[index]+lefttmove
        # intialzing the successor move
        new_state[index] = newstate
        new_state = tuple(new_state)  # the tuple of state to be returned

        return new_state
        # return newstate

    # This function returns the cost of applying the given action to the given state

    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # TODO: ADD YOUR CODE HERE
        currCost = 0
        newstate = None
        new_state = list(state)
        index, dir = action
        rightmove = Point(1, 0)
        lefttmove = Point(-1, 0)
        upmove = Point(0, -1)
        downmove = Point(0, 1)
        if dir == Direction.DOWN:
            newstate = state[index]+downmove
        if dir == Direction.UP:
            newstate = state[index]+upmove
        if dir == Direction.RIGHT:
            newstate = state[index]+rightmove
        if dir == Direction.LEFT:
            newstate = state[index]+lefttmove

        new_state[index] = newstate
        new_state = tuple(new_state)
        # check if the new state is possible , not a wall and not another car's slot , if yes
        if newstate in self.passages:
            # convert the position to chr accordingly to realize the cost of moving
            currCost += self.values[chr(index + ord('A'))]

        if newstate in self.slots.keys():  # check if the new state is already another car's slot to pay the 100 cost of getting in another car's room
            if index != self.slots[newstate]:

                currCost += 100

        return currCost

    # Read a parking problem from text containing a grid of tiles

    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip()
                                   for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
