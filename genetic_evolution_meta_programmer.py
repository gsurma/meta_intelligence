import brainfuck_interpreter as brainfuck
import random
import copy
import numpy as np
from statistics import mean
import sys
import time
import matplotlib.pyplot as plt

ASCII_CHARS_COUNT = 256
AVAILABLE_OPS = [">", # Increment the pointer.
 				 "<", # Decrement the pointer.
 				 "+", # Increment the byte at the pointer.
 				 "-", # Decrement the byte at the pointer.
 				 ".", # Output the byte at the pointer.
 				 "[", # Jump forward past the matching ] if the byte at the pointer is zero.
 				 "]"] # Jump backward to the matching [ unless the byte at the pointer is zero.
				 #"," #Input a byte and store it in the byte at the pointer. (Since we don't want any inputs, let's skip it as for now)


POPULATION = 100
MUTATION_RATE = 0.115
MAX_MUTATION_ATTEMPTS = 500
SELECTION_RATE = 0.9
TOP_PERFORMERS_COUNT = int(POPULATION * SELECTION_RATE)
PROGRAM_LENGTH_LOWER_BOUND = 10
PROGRAM_LENGTH_UPPER_BOUND = 100
OUTPUT_DIR = "./output/"

class GeneticEvolutionMetaProgrammer():

	target = ""
	generation = 0
	population = []
	max_fitness_score = 0
	start_time = None
	best_fitness_scores = []

	def __init__(self, target):
		self.target = target
		self.max_fitness_score = len(self.target)*ASCII_CHARS_COUNT
		self.start_time = time.time()

		print("Started looking for: " + repr(target))
		self.genetic_evolution()

	def genetic_evolution(self):
		self.population = self.generate_population(self.population)
		while True:
			print("\ngeneration: " + str(self.generation) + ", population: " + str(len(self.population)) + ", mutation_rate: " + str(MUTATION_RATE))
			
			# 1. Selection
			elite = self.select_elite(self.population)

			# 2. Crossover (Roulette selection)
			pairs = self.generate_pairs(elite)
			selected_offsprings = []
			for pair in pairs:
				offsprings = self.crossover(pair[0][0], pair[1][0])
				selected_offsprings.append(offsprings[random.randint(0, 1)])

			# 3. Mutation
			mutated_population = self.mutation(selected_offsprings)

			# 4. Validation (We don't want syntactically incorrect programs)
			valid_population = []
			for chromosome in mutated_population:
				if brainfuck.evaluate(chromosome) is not None:
					valid_population.append(chromosome)
			print("propagated to next generation: " + str(len(valid_population)))
			self.population = self.generate_population(valid_population)
			self.generation += 1

	def generate_population(self, population):
		while len(population) < POPULATION:
			length = random.randint(PROGRAM_LENGTH_LOWER_BOUND, PROGRAM_LENGTH_UPPER_BOUND)
			chromosome = ""
			for i in range(0, length):
				chromosome += random.choice(AVAILABLE_OPS)
			if brainfuck.evaluate(chromosome) is not None: # We don't want programs that are syntactically incorrect
				population.append(chromosome)
		return population

	def fitness_score(self, input_string, target):
		fitness_score = 0
		for i, c in enumerate(input_string):
			input_score = ord(c)
			if len(target) > i:
				target_score = ord(target[i])
				fitness_score += ASCII_CHARS_COUNT-abs(input_score-target_score)
		length_diff = abs(len(target)-len(input_string))
		for _ in range(0, length_diff):
			fitness_score -= ASCII_CHARS_COUNT
		return fitness_score

	def select_elite(self, population):
		scores_for_chromosomes = []
		for i in range(0, len(population)):
			chromosome = population[i]
			result = brainfuck.evaluate(chromosome)
			score = self.fitness_score(result, self.target)
			if score == self.max_fitness_score:
				current_time = time.time()
				print("\nFOUND SOLUTION: " + chromosome + " for: " + repr(self.target) +  " in: " + str(int((current_time-self.start_time)/60)) + " minutes")
				self.best_fitness_scores.append(self.max_fitness_score)
				self.update_fitness_plot()
				exit()
			scores_for_chromosomes.append((chromosome, score))
		scores_for_chromosomes.sort(key=lambda x: x[1])
		scores = [x[1] for x in scores_for_chromosomes]
		print("population: " + "(min: " + str(min(scores)) + ", avg: " + str(mean(scores)) + ", max: " + str(max(scores)) + ")")

		top_performers = scores_for_chromosomes[-TOP_PERFORMERS_COUNT:]
		top_scores = [x[1] for x in top_performers]
		print("elite " + str(round(1.0-SELECTION_RATE, 2)) + ": " + "(min: " + str(min(top_scores)) + ", avg: " + str(mean(top_scores)) + ", max: " + str(max(top_scores)) + ")")
		
		chromosome = top_performers[-1][0]
		result = brainfuck.evaluate(chromosome)
		best_fitness_score = self.fitness_score(result, self.target)
		print("best: " + chromosome + ", result: " + repr(result) + ", score: " + str(best_fitness_score) + "/" + str(self.max_fitness_score))

		self.best_fitness_scores.append(best_fitness_score)
		self.update_fitness_plot()
		
		return top_performers

	def generate_pairs(self, parents):
		normalized_parents = self.softmax([x[1] for x in parents])
		total_parents_score = sum(normalized_parents)
		pairs = []
		while len(pairs) < POPULATION:
			pair = self.pair(parents, normalized_parents, total_parents_score)
			if len(pair) == 2 and pair[0] is not None and pair[1] is not None:
				pairs.append(pair)
		return pairs

	def pair(self, parents, normalized_parents, total_parents_score):
		pick_parent_a = random.uniform(0, total_parents_score)
		pick_parent_b = random.uniform(0, total_parents_score)
		return [self.roulette_selection(parents, normalized_parents, pick_parent_a), self.roulette_selection(parents, normalized_parents, pick_parent_b)]

	def roulette_selection(self, parents, normalized_parents, pick):
		current = 0.0
		for i in range(0, len(parents)):
			current += normalized_parents[i]
			if current > pick:
				return parents[i]

	def crossover(self, x, y):
		offspring_x = x
		offspring_y = y
		length = min(len(x), len(y))
		for i in range(0, length):
			if random.choice([True, False]):
				crossover_at_index = self.crossover_at_index(offspring_x, offspring_y, i)
				offspring_x = crossover_at_index[0]
				offspring_y = crossover_at_index[1]
		return offspring_x, offspring_y

	def crossover_at_index(self, x, y, i):
		x_at_i = self.get_value_at_index(x, i)
		y_at_i = self.get_value_at_index(y, i)
		x = self.set_value_at_index(x, y_at_i, i)
		y = self.set_value_at_index(y, x_at_i, i)
		return x, y

	def mutation(self, selected_offsprings):
		offsprings = []
		for offspring in selected_offsprings:
			valid = False
			mutation_attempts = 0
			offspring_mutation = copy.deepcopy(offspring)
			while not valid and mutation_attempts < MAX_MUTATION_ATTEMPTS:
				for i in range(0, len(offspring_mutation)):
					if np.random.choice([True, False], p=[MUTATION_RATE, 1-MUTATION_RATE]):
						action_type = random.randint(0, 2)
						if action_type == 0 and len(offspring_mutation) < PROGRAM_LENGTH_UPPER_BOUND: 
							# Inserting random value at index
							offspring_mutation = offspring_mutation[:i] + random.choice(AVAILABLE_OPS) + offspring_mutation[i:]
						elif action_type == 1 and len(offspring_mutation) > PROGRAM_LENGTH_LOWER_BOUND: 
							# Removing value at index
							offspring_mutation = offspring_mutation[:i] + offspring_mutation[i+1:]
						else: 
							# Setting random value at index
							offspring_mutation = self.set_value_at_index(offspring_mutation, random.choice(AVAILABLE_OPS), i)
				if brainfuck.evaluate(offspring_mutation) is not None:
					valid = True
					offsprings.append(offspring_mutation)
				mutation_attempts += 1
		return offsprings

	def update_fitness_plot(self):
		plt.plot(self.best_fitness_scores, label="best_fitness")
		plt.plot([self.max_fitness_score for _ in range(0, len(self.best_fitness_scores))], label="max_fitness (" + str(self.max_fitness_score) + ")")
		plt.legend(loc='best')
		plt.title("Target: " + repr(self.target))
		plt.xlabel("Generation")
		plt.ylabel("Fitness")
		plt.savefig(OUTPUT_DIR + repr(self.target) + ".png", bbox_inches="tight")
		plt.close()

	def softmax(self, x):
		y = np.exp(x - np.max(x))
		return y / y.sum()

	def get_value_at_index(self, string, i):
		try:
			return string[i]
		except IndexError:
			return None

	def set_value_at_index(self, string, value, i):
		if i > len(string):
			return string
		elif value is not None:
			return string[:i] + value + string[i+1:]
		else:
			return string

if __name__ == "__main__":
	if len(sys.argv) == 2:
		GeneticEvolutionMetaProgrammer(str(sys.argv[1]))
	else: 
		print("Usage: python3 ", sys.argv[0], " <text_to_find>")
	
