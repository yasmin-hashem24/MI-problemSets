from typing import Tuple, List, Callable, Any
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint, Constraint

# TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs


def check_condition(c1, c2) -> bool:
    return c1[0] + c1[1] + c1[2] == c2[0] + 10 * c2[1]


class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS
        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        # create the variables
        variables = set(LHS0 + LHS1 + RHS)

        # loop over variables
        # create constraints between variables to all have distinct
        covered = set()
        for var in variables:
            for varAgain in variables:
                if (var != varAgain):
                    if (((var, varAgain) or (varAgain, var)) not in covered):
                        covered.add((var, varAgain))
                        problem.constraints.append(BinaryConstraint(
                            (var, varAgain), lambda c1, c2: c1 != c2))

        # create the domain for each variable
        domains = {}
        for letter in variables:
            if letter == LHS0[0] or letter == LHS1[0] or letter == RHS[0]:
                domains[letter] = {
                    (item3) for item3 in range(1, 10)}
            elif letter in LHS0[1:] + LHS1[1:] + RHS[1:]:
                domains[letter] = {
                    (item3) for item3 in range(0, 10)}

        # create the binary constraints
        newCons1 = []
        carry_varadv = f'c{len(RHS)-1}'
        domains[carry_varadv] = {(item3) for item3 in range(0, 2)}
        for letter in reversed(range(len(LHS0))):
            # create variables for the current sum and carry
            carry_var = f'c{letter}'
            variables.add(carry_var)
            domains[carry_var] = {(item3) for item3 in range(0, 2)}
            # create a constraint for the current sum and carry
            if letter == len(LHS0)-1:
                con1_tuple = LHS0[letter] + LHS1[letter]
                domains[con1_tuple] = {(item, item2) for item in domains[LHS0[letter]]
                                       for item2 in domains[LHS1[letter]]}
                problem.constraints.append(BinaryConstraint(
                    (LHS0[letter], con1_tuple), lambda c1, c2: c1 == c2[0]))
                problem.constraints.append(BinaryConstraint(
                    (LHS1[letter], con1_tuple), lambda c1, c2: c1 == c2[1]))

            else:
                con1_tuple = LHS0[letter]+LHS1[letter]+carry_varadv
                domains[con1_tuple] = {(item, item2, item3) for item in domains[LHS0[letter]]
                                       for item2 in domains[LHS1[letter]] for item3 in range(0, 2)}
                problem.constraints.append(BinaryConstraint(
                    (LHS0[letter], con1_tuple), lambda c1, c2: c1 == c2[0]))
                problem.constraints.append(BinaryConstraint((
                    LHS1[letter], con1_tuple), lambda c1, c2: c1 == c2[1]))
                problem.constraints.append(BinaryConstraint((
                    carry_var, con1_tuple), lambda c1, c2: c1 == c2[2]))
            newCons1.append(con1_tuple)
            variables.add(con1_tuple)
            carry_varadv = carry_var

        newCons2 = []
        for letter in reversed(range(len(RHS))):
            # create variables for the current sum and carry
            carry_var = f'c{letter-1}'
            if letter == 0:
                con1_tuple = RHS[letter]+f'c{0}'
                domains[con1_tuple] = {
                    (item, item3) for item in domains[RHS[letter]] for item3 in range(0, 2)}
                problem.constraints.append(BinaryConstraint(
                    (RHS[letter], con1_tuple), lambda c1, c2: c1 == c2[0]))
                problem.constraints.append(BinaryConstraint((
                    f'c{0}', con1_tuple), lambda c1, c2: c1 == c2[1]))
            else:
                con1_tuple = RHS[letter]+carry_var
                domains[con1_tuple] = {
                    (item, item3) for item in domains[RHS[letter]] for item3 in range(0, 2)}
                problem.constraints.append(BinaryConstraint(
                    (RHS[letter], con1_tuple), lambda c1, c2: c1 == c2[0]))
                problem.constraints.append(BinaryConstraint(
                    (carry_var, con1_tuple), lambda c1, c2: c1 == c2[1]))

            newCons2.append(con1_tuple)
            variables.add(con1_tuple)

        for element in reversed(range(len(newCons2))):
            if (element == 0):
                problem.constraints.append(BinaryConstraint(
                    (newCons1[element], newCons2[element]), lambda c1, c2: c1[0]+c1[1] == c2[0]+10*c2[1]))
            elif (element == len(newCons2)-1):
                problem.constraints.append(BinaryConstraint(
                    (newCons1[element-1], newCons2[element]), lambda c4, c5: c5[0] == c5[1]))
            else:
                problem.constraints.append(BinaryConstraint(
                    (newCons1[element], newCons2[element]), lambda c1, c2: c1[0]+c1[1]+c1[2] == c2[0]+10*c2[1]))

        problem.variables = list(variables)
        problem.domains = domains

        return problem

    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
