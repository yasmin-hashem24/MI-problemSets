from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented
import queue
from queue import PriorityQueue, Queue
# TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    explored = set()
    pathe = []  # action path
    path = []  # stetes path
    # node = [initial_state]
    frontier = [initial_state]  # list of states FIFO

    # list of parents of each node
    parents = {initial_state: ('null', initial_state)}

    while frontier:
        # last state in FIFO
        node = frontier.pop(0)
        if node not in explored:  # add to visitied if not have been before , check and do else

            explored.add(node)
        else:  # to avoid double expansion
            continue

        # loop over possible actions from a state
        for action in problem.get_actions(node):

            # get successor of current node
            child = problem.get_successor(node, action)
            if child == action:
                flag = 0  # graph #know the kind of question to see if return states or paths
            else:
                flag = 1  # suko

            if child not in explored and child not in frontier:
                if problem.is_goal(child):  # if goal reached
                    if flag == 0:
                        # intialize parent of current child
                        parents[child] = (node, action)
                        path.append(child)
                        newnode = path[0]
                        parent = parents[newnode]
                        prev = parent[0]

                        while prev != initial_state:
                            path.append(prev)  # append the state
                            parent = parents[prev]  # fro looping
                            prev = parent[0]

                        path.reverse()
                        return path

                    else:
                        pathe.append(action)  # append the action case of suko
                        parent_tuple = parents[node]  # parent of that child
                        parent = parent_tuple[0]
                        actioon = parent_tuple[1]
                        while parent != 'null':
                            # getting parent of the node called parent "originally was child"
                            pathe.append(actioon)
                            # parent is a key tuple and we want it equal to first element only
                            parent_tuple = parents[parent]
                            parent = parent_tuple[0]
                            actioon = parent_tuple[1]

                        pathe.reverse()
                        return pathe
                        # explored.add(child)
                else:

                    parents[child] = (node, action)  # intialize parent
                    frontier.append(child)  # add to frontier and move forword

    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    explored = set()
    pathe = []  # action path
    path = []  # stetes path
    # node = [initial_state]
    frontier = [initial_state]  # list of states FIFO

    # list of parents of each node
    parents = {initial_state: ('null', initial_state)}

    while frontier:
        # last state in FIFO
        node = frontier.pop(-1)
        if node not in explored:  # add to visitied if not have been before , check and do else

            explored.add(node)
        else:  # to avoid double expansion
            continue

        if problem.is_goal(node):  # if goal reached
            if flag == 0:
                # intialize parent of current child

                path.append(node)
                newnode = path[0]
                parent = parents[newnode]
                prev = parent[0]

                while prev != initial_state:
                    path.append(prev)  # append the state
                    parent = parents[prev]  # fro looping
                    prev = parent[0]

                path.reverse()
                return path

            else:

                parent_tuple = parents[node]  # parent of that child
                parent = parent_tuple[0]
                actioon = parent_tuple[1]
                while parent != 'null':
                    # getting parent of the node called parent "originally was child"
                    pathe.append(actioon)
                    # parent is a key tuple and we want it equal to first element only
                    parent_tuple = parents[parent]
                    parent = parent_tuple[0]
                    actioon = parent_tuple[1]

                pathe.reverse()
                return pathe
                # explored.add(child)

        # loop over possible actions from a state
        for action in problem.get_actions(node):

            # get successor of current node
            child = problem.get_successor(node, action)
            if child == action:
                flag = 0  # graph #know the kind of question to see if return states or paths
            else:
                flag = 1  # suko

            if child not in explored:

                parents[child] = (node, action)  # intialize parent
                frontier.append(child)  # add to frontier and move forword

    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:

    explored = set()
    exploredOrder = {}
    order = 0
    pathe = []
    explored = {}
    explored[initial_state] = 0
    exploredOrder[initial_state] = 0
    frontier = queue.PriorityQueue()
    frontier.put((0, order, initial_state))
    parents = {initial_state: ('null', initial_state)}

    while not frontier.empty():

        dequeued_item = frontier.get()
        node = dequeued_item[2]
        nodePri = dequeued_item[0]
        if problem.is_goal(node):
            if flag == 0:
                path = [node]
                prev = node

                while prev != initial_state:
                    parent = parents[prev][0]
                    path.append(parent)
                    prev = parent

                path.reverse()
                path.pop(0)
                return path

            else:
                parent_tuple = parents[node]  # parent of that child
                parent = parent_tuple[0]
                actioon = parent_tuple[1]
                while parent != 'null':
                    # getting parent of the node called parent "originally was child"
                    pathe.append(actioon)
                    # parent is a key tuple and we want it equal to first element only
                    parent_tuple = parents[parent]
                    parent = parent_tuple[0]
                    actioon = parent_tuple[1]
                # end of while

                pathe.reverse()
                return pathe

        else:

            for action in problem.get_actions(node):

                child = problem.get_successor(node, action)
                if child == action:
                    flag = 0  # graph
                else:
                    flag = 1  # dung
                frontierlist = list(frontier.queue)
                if child not in explored:
                    # explored.add(child)
                    explored[child] = nodePri+problem.get_cost(child, action)
                    order += 1
                    exploredOrder[child] = order
                    parents[child] = (node, action)
                    frontier.put(
                        (nodePri+problem.get_cost(child, action), order, child))

                elif does_exist(frontierlist, child):
                    if nodePri+problem.get_cost(child, action) < explored[child]:

                        frontier.queue.remove(
                            (explored[child], exploredOrder[child], child))
                        frontier.put(
                            (nodePri+problem.get_cost(child, action), order, child))

                        parents[child] = (node, action)

        # return None


def does_exist(flist: list, child_node: S) -> bool:
    # check
    for item in flist:
        if item[2] == child_node:
            return True
        else:
            continue
    return False
# end of does_exist function


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    explored = set()
    exploredOrder = {}
    order = 0
    pathe = []
    explored = {}
    explored[initial_state] = 0
    exploredOrder[initial_state] = 0
    frontier = queue.PriorityQueue()
    frontier.put((0, order, initial_state))
    parents = {initial_state: ('null', initial_state)}
    path = []
    while not frontier.empty():

        dequeued_item = frontier.get()
        node = dequeued_item[2]
        nodePri = dequeued_item[0]
        if problem.is_goal(node):
            if flag == 0:
                path.append(node)
                curr = path[0]
                parent = parents[curr]
                prev = parent[0]

                while prev != 'null':

                    path.append(prev)
                    parent = parents[prev]
                    prev = parent[0]

                path.reverse()
                path.pop(0)
                return path

            else:
                parent_tuple = parents[node]  # parent of that child
                parent = parent_tuple[0]
                actioon = parent_tuple[1]
                while parent != 'null':
                    # getting parent of the node called parent "originally was child"
                    pathe.append(actioon)
                    # parent is a key tuple and we want it equal to first element only
                    parent_tuple = parents[parent]
                    parent = parent_tuple[0]
                    actioon = parent_tuple[1]
                # end of while

                pathe.reverse()
                return pathe

        else:

            for action in problem.get_actions(node):

                child = problem.get_successor(node, action)
                if child == action:
                    flag = 0  # graph
                else:
                    flag = 1  # dung
                frontierlist = list(frontier.queue)
                if child not in explored and not frontier.queue.__contains__(child):
                    # explored.add(child)
                    explored[child] = problem.get_cost(
                        child, action) + heuristic(problem, child)
                    order += 1
                    exploredOrder[child] = order
                    parents[child] = (node, action)
                    frontier.put(
                        (heuristic(problem, child)+problem.get_cost(child, action) + heuristic(problem, child), order, child))

                elif does_exist(frontierlist, child):
                    if (problem.get_cost(child, action) + heuristic(problem, child)) < explored[child]:

                        frontier.queue.remove(
                            (explored[child], exploredOrder[child], child))
                        frontier.put(
                            (problem.get_cost(child, action) + heuristic(problem, child)), order, child)

                        parents[child] = (node, action)

        # return None


def does_exist(flist: list, child_node: S) -> bool:
    # check
    for item in flist:
        if item[2] == child_node:
            return True
        else:
            continue
    return False
# end of does_exist function


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    explored = set()
    exploredOrder = {}
    order = 0
    pathe = []
    explored = {}
    explored[initial_state] = 0
    exploredOrder[initial_state] = 0
    frontier = queue.PriorityQueue()
    frontier.put((0, order, initial_state))
    parents = {initial_state: ('null', initial_state)}

    while not frontier.empty():

        dequeued_item = frontier.get()
        node = dequeued_item[2]
        nodePri = dequeued_item[0]
        if problem.is_goal(node):
            if flag == 0:
                path = [node]
                prev = node

                while prev != initial_state:
                    parent = parents[prev][0]
                    path.append(parent)
                    prev = parent

                path.reverse()
                path.pop(0)
                return path

            else:
                parent_tuple = parents[node]  # parent of that child
                parent = parent_tuple[0]
                actioon = parent_tuple[1]
                while parent != 'null':
                    # getting parent of the node called parent "originally was child"
                    pathe.append(actioon)
                    # parent is a key tuple and we want it equal to first element only
                    parent_tuple = parents[parent]
                    parent = parent_tuple[0]
                    actioon = parent_tuple[1]
                # end of while

                pathe.reverse()
                return pathe

        else:

            for action in problem.get_actions(node):

                child = problem.get_successor(node, action)
                if child == action:
                    flag = 0  # graph
                else:
                    flag = 1  # dung
                frontierlist = list(frontier.queue)
                if child not in explored:
                    # explored.add(child)
                    explored[child] = problem.get_cost(
                        child, node)+heuristic(problem, child)
                    order += 1
                    exploredOrder[child] = order
                    parents[child] = (node, action)
                    frontier.put(
                        (problem.get_cost(child, node)+heuristic(problem, child), order, child))

                elif does_exist(frontierlist, child):
                    if problem.get_cost(child, node)+heuristic(problem, child) < explored[child]:

                        frontier.queue.remove(
                            (explored[child], exploredOrder[child], child))
                        frontier.put(
                            (problem.get_cost(child, node)+heuristic(problem, child), order, child))

                        parents[child] = (node, action)

        # return None


def does_exist(flist: list, child_node: S) -> bool:
    # check
    for item in flist:
        if item[2] == child_node:
            return True
        else:
            continue
    return False
# end of does_exist function
