from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint, Constraint
from helpers.utils import NotImplemented
from copy import deepcopy
# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.


def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {
            value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic,
#       we order them in the same order in which they appear in "problem.variables".


def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(
        problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.


def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    # create an assignment dictionary with the variable and value

    for constraint in problem.constraints:  # loop on each constraint in the assigned problem with the new variable
        # check if the constraint involves the assigned variable
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:
            # Get the other involved variable.
            other_variable = constraint.get_other(assigned_variable)
            if other_variable not in domains:
                continue  # If the other variable has no domain, skip
            # define a list for editing and removing
            other_domain = list(domains[other_variable])
            to_remove = [value for value in other_domain if not constraint.condition(
                assigned_value, value)]  # Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
            for value in to_remove:
                other_domain.remove(value)
            if not other_domain:  # no possible solution due to the assignment
                return False
            # now update the domains with the final set we got to after removal that is not empty
            domains[other_variable] = set(other_domain)
            # convert to set cause list gives error

    return True  # we r out with no empty domains each got assignmed with the new assignemnt


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.s
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic,
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.

def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    value_counts = {}

    # Initialize a dictionary to store the number of constraints each value would violate if assigned.
    # This dictionary will be used to sort the values in ascending order of their constraint counts.

    # Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
    new_domains = domains.copy()
    # since they contain the current domains of unassigned variables only.
    # you do not modify the given domains. But you can create and modify a copy.

    for value in domains[variable_to_assign]:
        # for each value, create a temporary copy of the domains dictionary
        temp_domains = new_domains.copy()
        # assign the current value to the variable in the new copy
        temp_domains[variable_to_assign] = {value}

        count = 0  # initialize count of constraints that would be violated by this assignment

        for constraint in problem.constraints:  # loop over each constraint in the problem

            if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:
                # if the constraint involves the assigned variable, check if it would be violated by the current assignment
                other_variable = constraint.get_other(variable_to_assign)
                if other_variable not in temp_domains:
                    continue  # If the other variable has no domain, skip

                for other_value in temp_domains[other_variable]:
                    if not constraint.is_satisfied({variable_to_assign: value, other_variable: other_value}):
                        count += 1  # If the constraint is not satisfied, increment the count of violated constraints

        # store the count of violated constraints for the current value
        value_counts[value] = count

    # sort according to the heuristic
    sorted_values = sorted(
        domains[variable_to_assign], key=lambda v: value_counts.get(v, 0))

    return sorted_values

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.

# backtracking funtion that uses minimum_remaining_values and least_restraining_values and forward_checking
# check if the variable to be assigned and value to assign satisfies all constraints with variables and values already assigned


# check if the variable to be assigned and value to assign satisfies all constraints with variables and values already assigned
def check_constraints(assignment: Assignment, problem: Problem, variable_to_assign: str, value_to_assign: Any):
    if assignment == {}:
        return True
    related_constraints = []
    for con in problem.constraints:  # get related constraints to variable to be assigned
        if con == variable_to_assign:
            related_constraints.append(con)
    for con in related_constraints:
        other = con.get_other(variable_to_assign)
        if other in assignment.keys():
            # if value to be assigned does not satisfy a constraint with variables already assigned
            if con.is_satisfied({variable_to_assign: value_to_assign, other: assignment[other]}) == False:
                return False  # return false indicating that this assignment will not work
    return True  # else return true

# backtracking funtion that uses minimum_remaining_values and least_restraining_values and forward_checking


def backtrack(assignment: Assignment, problem: Problem, domains: Dict[str, set]):
    # base case all variables are assigned return assignment
    if problem.is_complete(assignment):
        return assignment
    # choose a variable with the least remaining values
    var = minimum_remaining_values(problem, domains)
    # sort list of values according to the least restaining and loop
    for val in least_restraining_values(problem, var, domains):
        assignment[var] = val  # test assign variable with values
        # save current domain to undo deletion, deepcopy is used to ensure a complete separate copy of dict domains
        current_domains_state = deepcopy(domains)
        # delete domain of variable to only keep the domain of the unassigned variables
        del domains[var]
        # check assignment of the variable goes with the values of previously assigned vars
        if check_constraints(assignment, problem, var, val):
            # apply forward checking and if there is no empty domain after continue
            if forward_checking(problem, var, val, domains):
                # apply this assignment permenantly and recusrive call to assign rest of variables
                result = backtrack(assignment, problem, domains)
                if result != None:
                    return result  # if there is a possible assignment return assignment
        domains = current_domains_state  # else undo changes in domain
        del assignment[var]  # unassign the variable and loop on another value
    return None  # if ther is no possible assignment return false


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#           XX Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    if one_consistency(problem) == False:  # calling one_consistency once intially
        return None  # if one of the domains became empty return None i.e. no possible assignment
    # used a temporary domain instead of problem.domains, used deep copy again to ensure a complete separate copy of dict domains
    domains = deepcopy(problem.domains)
    # initial call to backtrack with empty assignment
    return backtrack({}, problem, domains)
