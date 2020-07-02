import unittest
from pkg.spea2.spea2 import Spea2 
from pkg.problem.problem import Problem 
from pkg.problem.constraint import Constraint
from pkg.problem.variable import Variable

class Spea2Test(unittest.TestCase):
    def defaultVariables(self):
        return [
            Variable([0, 1, 2]),
            Variable([0, 1, 2]),
            Variable([0, 1, 2]),
        ]

    def defaultConsistentProblem(self):
        variables = self.defaultVariables()
        variables[0].set_value(2)
        variables[1].set_value(1)
        variables[2].set_value(2)
        return Problem(
            variables,
            [
                Constraint((0, 2),
                           lambda variables: variables[0] == variables[1]),
                Constraint(tuple([1]), lambda variables: variables[0] == 1),
                Constraint(tuple([2]), lambda variables: variables[0] > 0)
            ], None)

    def test_solve(self):
        spea2 = Spea2(self.defaultConsistentProblem())
        spea2.solve()