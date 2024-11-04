import random
import numpy as np


# Define items with weights and values
items = [
    {"weight": 10, "value": 60},
    {"weight": 20, "value": 100},
    {"weight": 30, "value": 120}
]
knapsack_capacity = 50  # Maximum weight capacity of the knapsack

# Parameters for Genetic Algorithm
POPULATION_SIZE = 10
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1

# Fitness function: calculates total value if within weight capacity, else returns 0
def calculate_fitness(solution):
    total_weight = total_value = 0
    for i, selected in enumerate(solution):
        if selected:
            total_weight += items[i]["weight"]
            total_value += items[i]["value"]
    
    # If the total weight exceeds the knapsack capacity, the fitness is zero
    if total_weight > knapsack_capacity:
        return 0
    return total_value

# Initialize population with random solutions (0 or 1 for each item)
def initialize_population():
    population = []
    for _ in range(POPULATION_SIZE):
        solution = [random.choice([0, 1]) for _ in items]
        population.append(solution)
    return population

# Selection (Roulette Wheel Selection)
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choice(population)  # Avoid division by zero if all fitnesses are 0

    selection_probs = [fitness / total_fitness for fitness in fitness_scores]
    return population[np.random.choice(len(population), p=selection_probs)]

# Crossover (Single-Point Crossover)
def single_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(items) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutation (Flip Mutation)
def mutate(solution):
    for i in range(len(solution)):
        if random.random() < MUTATION_RATE:
            solution[i] = 1 - solution[i]  # Flip 0 to 1 or 1 to 0

# Main Genetic Algorithm function
def genetic_algorithm():
    # Initialize population
    population = initialize_population()

    for generation in range(NUM_GENERATIONS):
        # Calculate fitness for each solution in the population
        fitness_scores = [calculate_fitness(solution) for solution in population]

        # Create a new population
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            # Selection
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)

            # Crossover
            child1, child2 = single_point_crossover(parent1, parent2)

            # Mutation
            mutate(child1)
            mutate(child2)

            # Add offspring to new population
            new_population.extend([child1, child2])

        # Replace old population with new population
        population = new_population

    # Find the best solution in the final population
    best_solution = max(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_solution)
    best_weight = sum(items[i]["weight"] for i in range(len(items)) if best_solution[i] == 1)
    
    return best_solution, best_fitness, best_weight

# Run Genetic Algorithm
best_solution, best_fitness, best_weight = genetic_algorithm()
print("Best Solution:", best_solution)
print("Total Value:", best_fitness)
print("Total Weight:", best_weight)
