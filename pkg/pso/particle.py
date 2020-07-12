import random
import copy
from pkg.problem.compare import dominates

DRAG = 0.5
SOCIAL_SCALE = 1.5
COGNITIVE_SCALE = 1.5

class Particle:
    def __init__(self, problem):
        self.problem = problem
        self.best = copy.deepcopy(problem)
        self.velocity = [0 for _ in range(problem.num_variables())]
    
    def move(self):
        for i in range(self.problem.num_variables()):
            self.problem.set_value(i, self.problem.closest_in_domain(i, self.velocity[i] + self.problem.get_value(i)))
    
    def accelerate(self):
        for i in range(self.problem.num_variables()):
            self.velocity[i] = (DRAG * self.velocity[i]) + (SOCIAL_SCALE * random.randrange(0.0, 1.0) * (self.best.get_value(i) - self.problem.get_value(i))) + (COGNITIVE_SCALE * random.randrange(0.0, 1.0) * (self.best.get_value(i) - self.problem.get_value(i)))

    def update_best(self):
        if dominates(self.problem.objective_values(), self.best.objective_values()):
            self.best = copy.deepcopy(self.problem)

    def get_best(self):
        return self.best

    def get_problem(self):
        return self.problem

