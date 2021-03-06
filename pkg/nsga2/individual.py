from pkg.random.random import Random
from pkg.problem.compare import dominates
from pkg.consts import Constants
from math import floor


class Individual:
    def __init__(self, problem=None, individual=None):
        if problem is None and individual is None:
            raise ValueError("must have a problem or an individual")
        elif problem is not None and individual is not None:
            raise ValueError("must have one of a problem or an individual")
        if problem is not None:
            self.problem = problem
            self.dominates = set()
            self.domination_count = 0
            self.crowding_distance = 0
            self.inverse_tournament_rank = 0
            self.rank = None
        elif individual is not None:
            self.problem = individual.problem
            self.dominates = individual.dominates
            self.domination_count = individual.domination_count
            self.crowding_distance = individual.crowding_distance
            self.inverse_tournament_rank = individual.inverse_tournament_rank
            self.rank = individual.rank

    def __str__(self):
        return str(self.problem.variable_assignments())

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def does_dominate(self, q):
        return dominates(self.problem.objective_values(), q.problem.objective_values())

    def add_dominated(self, q):
        self.dominates.add(q)

    def get_dominates(self):
        return self.dominates

    def increment_dominated(self):
        self.domination_count += 1

    def set_rank(self, rank):
        self.rank = rank

    def is_dominated(self):
        return self.domination_count != 0

    def get_dominated(self):
        return self.dominates

    def get_problem(self):
        return self.problem

    def decrement_dominated(self):
        if self.domination_count > 0:
            self.domination_count -= 1

    def set_crowding_distance(self, crowding_distance):
        self.crowding_distance = crowding_distance

    def get_crowding_distance(self):
        return self.crowding_distance

    def get_objective_values(self):
        return self.problem.objective_values()

    def set_inverse_tournament_rank(self, inverse_tournament_rank):
        self.inverse_tournament_rank = inverse_tournament_rank

    def get_inverse_tournament_rank(self):
        return self.inverse_tournament_rank

    def swap_half_genes(self, other):
        while True:
            for _ in range(floor(self.problem.num_variables() / 2)):
                random_index = Random.random_int_between_a_and_b(0, self.problem.num_variables() - 1)
                self.problem.set_value(random_index, other.problem.get_value(random_index))
            if self.problem.consistent():
                break

    def emo_phase(self):
        for _ in range(Constants.NSGA2_NUM_GENES_MUTATING):
            random_index = Random.random_int_between_a_and_b(
                0, self.problem.num_variables() - 1)
            new_value = self.problem.closest_in_domain(random_index, self.problem.get_value(
                random_index) + Random.random_float_between_a_and_b(-Constants.NSGA2_MUTATION_STRENGTH, Constants.NSGA2_MUTATION_STRENGTH))
            if (self.problem.will_be_consistent(random_index, new_value)):
                self.problem.set_value(random_index, new_value)
