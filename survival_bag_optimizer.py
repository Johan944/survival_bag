import random
import numpy as np
import matplotlib.pyplot as plt

class SurvivalBagOptimizer:
    def __init__(self, items, max_weight, parameters, verbose=False):
        self._items = items
        self._items_names = list(items.keys())
        self._nb_items = len(self._items_names)
        self._max_weight = max_weight
        self._nb_individuals = parameters["nb_individuals"]
        self._nb_generations = parameters["nb_generations"]
        self._mutation_rate = parameters["mutation_rate"]
        self._pick_percentage = parameters["pick_percentage"]
        self._elite_percentage = parameters["elite_percentage"]

        self._population = []
        self._fitnesses = []
        self._best_fitness_per_generation = []

        self.verbose = verbose

    def _init_population(self):
        if self.verbose:
            print("Population Initialization.")
        self._population = []
        for _ in range(self._nb_individuals):
            current_individual = []
            for _ in self._items_names:
                current_individual.append(random.random() <= self._pick_percentage)
            self._population.append(current_individual)

    def _compute_fitnesses(self):
        if self.verbose:
            print("Compute fitnesses.")
        self._fitnesses = []
        for individual in self._population:
            current_fitness = 0
            current_weight = 0
            for item_name, keep in zip(self._items_names, individual):
                if keep:
                    current_fitness += self._items[item_name]["value"]
                    current_weight += self._items[item_name]["weight"]
            if current_weight > self._max_weight:
                current_fitness = 0
            self._fitnesses.append(current_fitness)
        if self.verbose:
            self.get_best_fitness()

    def _elite_selection(self):
        elites = []

        nb_individuals_to_keep = round(self._nb_individuals * self._elite_percentage)
        
        if nb_individuals_to_keep > 0:
            while len(elites) < nb_individuals_to_keep:
                best_fitness = -1
                best_individual = None
                for fitness, individual in zip(self._fitnesses, self._population):
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_individual = individual
                elites.append(best_individual)
        return elites

    def _tournament_selection(self):
        if self._nb_individuals > 2:
            sum_fitnesses = sum(self._fitnesses)
            selection_probabilities = [fitness / sum_fitnesses for fitness in self._fitnesses]
            first_individual_idx = np.random.choice(range(self._nb_individuals), p=selection_probabilities)
            second_individual_idx = first_individual_idx
            while second_individual_idx == first_individual_idx:
                second_individual_idx = np.random.choice(self._nb_individuals, p=selection_probabilities)
        elif self._nb_individuals == 2:
            first_individual_idx = 0
            second_individual_idx = 1
        return self._population[first_individual_idx], self._population[second_individual_idx]

    def _crossover(self):
        if self.verbose:
            print("Crossover.")
        if self._nb_individuals > 1:
            elites = self._elite_selection()
            if self.verbose:
                print("Number of elites choosen: ", len(elites))

            new_population = elites

            while len(new_population) < self._nb_individuals:
                first_individual, second_individual = self._tournament_selection()

                child = []
                cut_idx = random.randint(1, self._nb_items - 1)
                idx = 0

                while idx <= cut_idx:
                    child.append(first_individual[idx])
                    idx += 1
                while idx < self._nb_items:
                    child.append(second_individual[idx])
                    idx += 1
                new_population.append(child)
            self._population = new_population

    def _mutation(self):
        if self.verbose:
            print("Mutation")
        for individual in self._population:
            if random.random() < self._mutation_rate:
                idx_to_mutate = random.randint(0, self._nb_items - 1)
                individual[idx_to_mutate] = not individual[idx_to_mutate]

    def get_best_fitness(self):
        best_fitness = -1
        best_weight = -1
        best_individual = None
        best_items = []

        for idx in range(self._nb_individuals):
            if self._fitnesses[idx] > best_fitness:
                best_fitness = self._fitnesses[idx]
                best_individual = self._population[idx]
                best_items = []
                best_weight = 0
                for item_name, keep in zip(self._items_names, best_individual):
                    if keep:
                        best_items.append(item_name)
                        best_weight += self._items[item_name]["weight"]
        if self.verbose:
            print("Best items : ", ", ".join(best_items))
            print("Best fitness : ", best_fitness)
            print("Total Weight : ", best_weight)
        return best_individual, best_fitness, best_items, best_weight

    def run(self):
        if self.verbose:
            print(f"--- Start Generation 1 ---")
        self._init_population()
        self._compute_fitnesses()
        self._best_fitness_per_generation.append(max(self._fitnesses))
        if self.verbose:
            print(f"--- End Generation 1 ---\n")
        for generation_idx in range(self._nb_generations - 1):
            if self.verbose:
                print(f"--- Start Generation {generation_idx + 2} ---")
            self._crossover()
            self._mutation()
            self._compute_fitnesses()
            self._best_fitness_per_generation.append(max(self._fitnesses))
            if self.verbose:
                print(f"--- End Generation {generation_idx + 2} ---\n")

    def display_graph(self):
        generations_ids = range(1, self._nb_generations + 1)
        x = np.array(generations_ids)
        y = np.array(self._best_fitness_per_generation)

        plt.title("Best fitness per generation")
        plt.plot(x, y)
        plt.xlabel("Generations")
        plt.ylabel("Best fitness")
        plt.show()


