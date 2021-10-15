import random
import time
import numpy as np
import matplotlib.pyplot as plt
import survival_bag_optimizer

class OptimizeSurvivalBagOptimizer:
    def __init__(self, items, max_weight, parameters, verbose=False):
        self._items = items
        self._max_weight = max_weight

        self._nb_generations = parameters["nb_generations"]
        self._nb_individuals = parameters["nb_individuals"]
        self._nb_repetitions = parameters["nb_repetitions"]
        self._elite_percentage = parameters["elite_percentage"]
        self._mutation_rate = parameters["mutation_rate"]

        self._population = []
        self._fitnesses = []
        self._best_fitness_per_generation = []

        self.verbose = verbose

    def _generate_random_parameters(self):
        return {
            "nb_individuals": random.randint(1, 100),
            "nb_generations": random.randint(1, 100),
            "mutation_rate": random.random(),
            "pick_percentage": random.random(),
            "elite_percentage": random.random(),
        }

    def _init_population(self):
        if self.verbose:
            print("Population Initialization.")
        self._population = []
        for _ in range(self._nb_individuals):
            self._population.append(self._generate_random_parameters())

    def _compute_fitnesses(self):
        if self.verbose:
            print("Compute fitnesses.")
        self._fitnesses = []
        best_fitness = -1
        for individual in self._population:
            sum_fitness = 0
            sum_time = 0
            current_instance = survival_bag_optimizer.SurvivalBagOptimizer(self._items, self._max_weight, individual)
            for _ in range(self._nb_repetitions):
                start_time = time.time()
                current_instance.run()
                _, current_fitness, _, _ = current_instance.get_best_fitness()
                sum_fitness += current_fitness
                sum_time += time.time() - start_time
            avr_fitness = sum_fitness / self._nb_repetitions
            if avr_fitness > best_fitness:
                best_fitness = avr_fitness
            self._fitnesses.append({"fitness": sum_fitness, "avr_fitness": avr_fitness, "avr_time": sum_time / self._nb_repetitions})
        self._best_fitness_per_generation.append(best_fitness)
        if self.verbose:
            self.get_best_fitness()

    def _elite_selection(self):
        elites = []

        nb_individuals_to_keep = round(self._nb_individuals * self._elite_percentage)

        while len(elites) < nb_individuals_to_keep:
            best_fitness = -1
            best_individual = None
            best_idx = 0
            idx = 0
            for fitness, individual in zip(self._fitnesses, self._population):
                if fitness["fitness"] > best_fitness:
                    best_fitness = fitness["fitness"]
                    best_individual = individual
                    best_idx = idx
                idx += 1
            elites.append(best_individual)
            del self._population[best_idx]
            del self._fitnesses[best_idx]
            idx += 1
        return elites

    def _crossover(self):
        if self.verbose:
            print("Crossover.")
        if self._nb_individuals > 1:
            elites = self._elite_selection()
            if self.verbose:
                print("Number of elites choosen: ", len(elites))

            past_population = self._population + elites

            new_population = elites

            while len(new_population) < self._nb_individuals:
                first_parent_idx = random.randint(0, self._nb_individuals - 1)
                second_parent_idx = first_parent_idx
                while second_parent_idx == first_parent_idx:
                    second_parent_idx = random.randint(0, self._nb_individuals - 1)
                first_individual = past_population[first_parent_idx]
                second_individual = past_population[second_parent_idx]

                params_names = list(first_individual.keys())
                nb_params = len(params_names)

                cut_name = random.choice(params_names)
                child = {}
                idx = 0
                while params_names[idx] != cut_name:
                    child[params_names[idx]] = first_individual[params_names[idx]]
                    idx += 1
                while idx < nb_params:
                    child[params_names[idx]] = second_individual[params_names[idx]]
                    idx += 1
                new_population.append(child)
            self._population = new_population

    def _mutation(self):
        if self.verbose:
            print("Mutation")
        for individual in self._population:
            if random.random() < self._mutation_rate:
                params_names = list(individual.keys())
                param_to_mutate = random.choice(params_names)
                random_params = self._generate_random_parameters()
                individual[param_to_mutate] = random_params[param_to_mutate]

    def get_best_fitness(self):
        best_fitness = {"fitness": -1}
        best_individual = None

        for idx in range(self._nb_individuals):
            if self._fitnesses[idx]["fitness"] > best_fitness["fitness"]:
                best_fitness = self._fitnesses[idx]
                best_individual = self._population[idx]
        if self.verbose:
            print("Best params : ", best_individual)
            print("Best fitness : ", best_fitness)
        return best_individual, best_fitness

    def run(self):
        if self.verbose:
            print(f"--- Start Generation 1 ---")
        self._init_population()
        self._compute_fitnesses()
        if self.verbose:
            print(f"--- End Generation 1 ---\n")
        for generation_idx in range(self._nb_generations - 1):
            if self.verbose:
                print(f"--- Start Generation {generation_idx + 2} ---")
            self._crossover()
            self._mutation()
            self._compute_fitnesses()
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