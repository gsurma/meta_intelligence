# > 	Increment the pointer.
# < 	Decrement the pointer.
# + 	Increment the byte at the pointer.
# - 	Decrement the byte at the pointer.
# . 	Output the byte at the pointer.
# , 	Input a byte and store it in the byte at the pointer.
# [ 	Jump forward past the matching ] if the byte at the pointer is zero.
# ] 	Jump backward to the matching [ unless the byte at the pointer is zero.

# https://copy.sh/brainfuck/text.html

import brainfuck2 as brainfuck
import random
import copy
import numpy as np
from statistics import mean
import sys

ASCII_CHARS_COUNT = 256
POPULATION = 1000
MUTATION_RATE = 0.1
SELECTION_RATE = 0.9
PARENTS_COUNT = int(POPULATION * SELECTION_RATE)

PROGRAM_LENGTH_LOWER_BOUND = 10
PROGRAM_LENGTH_UPPER_BOUND = 100

AVAILABLE_OPS = [">", "<", "+", "-", ".", "[", "]"] #","


class MetaProgrammer():

	target = ""
	generation = 0
	population = []
	max_fitness_score = 0

	def __init__(self, target):
		self.target = target
		self.max_fitness_score = len(self.target)*ASCII_CHARS_COUNT

		# chromosome = "+[----->+++<]>+.+." #hi
		# result = brainfuck.evaluate(chromosome)
		# print(result)
		# score = self.fitness_string(result, self.target)
		# print(score)
		# exit()
		self.genetic_evolution()

	def genetic_evolution(self):
		self.population = self.generate_population(self.population)
		while True:
			print("generation: " + str(self.generation) + ", population: " + str(len(self.population)) + ", mutation_rate: " + str(MUTATION_RATE))

			# 1. Selection
			parents = self.strongest_parents(self.population)

			# 2. Crossover (Roulette selection)
			pairs = self.generate_pairs(parents)
			selected_offsprings = []
			for pair in pairs:
				offsprings = self.crossover(pair[0][0], pair[1][0])
				selected_offsprings.append(offsprings[0])

			# 3. Mutation
			mutated_population = self.mutation(selected_offsprings)
			
			#4. Validation (We don't want syntactically incorrect programs)
			valid_population = []
			for chromosome in mutated_population:
				if brainfuck.evaluate(chromosome) is not None:
					valid_population.append(chromosome)
			self.population = self.generate_population(valid_population)
			self.generation += 1

	def mutation(self, selected_offsprings):
		offsprings = []
		for offspring in selected_offsprings:
			offspring_mutation = copy.deepcopy(offspring)
			for i in range(0, len(offspring_mutation)):
				if np.random.choice([True, False], p=[MUTATION_RATE, 1-MUTATION_RATE]):
					action_type = random.randint(0, 2)
					if action_type == 0 and len(offspring_mutation) < PROGRAM_LENGTH_UPPER_BOUND: #Adding random value at index
						offspring_mutation = offspring_mutation[:i] + random.choice(AVAILABLE_OPS) + offspring_mutation[i:]
					elif action_type == 1 and len(offspring_mutation) > PROGRAM_LENGTH_LOWER_BOUND: # Removing value at index
						offspring_mutation = offspring_mutation[:i] + offspring_mutation[i+1:]
					else: #Setting random value at index
						offspring_mutation = self.set_value_at_index(offspring_mutation, random.choice(AVAILABLE_OPS), i)
			offsprings.append(offspring_mutation)		
		return offsprings

	def crossover(self, x, y):
		offspring_x = x
		offspring_y = y
		# print("before x: ", offspring_x)
		# print("before y: ", offspring_y)
		length = max(len(x), len(y))
		for i in range(0, length):
			if random.choice([True, False]):
				#print(i)
				crossover_at_index = self.crossover_at_index(offspring_x, offspring_y, i)
				# print(crossover_at_index[0])
				# print(crossover_at_index[1])
				offspring_x = crossover_at_index[0]
				offspring_y = crossover_at_index[1]
		# print()
		# print("after x: ", offspring_x)
		# print("after y: ", offspring_y)
		# exit()
		return offspring_x, offspring_y

	def crossover_at_index(self, x, y, i):
		x_at_i = self.get_value_at_index(x, i)
		y_at_i = self.get_value_at_index(y, i)
		x = self.set_value_at_index(x, y_at_i, i)
		y = self.set_value_at_index(y, x_at_i, i)
		return x, y

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

	def strongest_parents(self, population):
		scores_for_chromosomes = []
		for i in range(0, len(population)):
			chromosome = population[i]
			result = brainfuck.evaluate(chromosome)
			score = self.fitness_string(result, self.target)
			if score == self.max_fitness_score:
				print("FOUND SOLUTION: " + chromosome + " for: " + self.target)
				exit()
			scores_for_chromosomes.append((chromosome, score))
		scores_for_chromosomes.sort(key=lambda x: x[1])
		print("population: " + str(mean([x[1] for x in scores_for_chromosomes])))

		top_performers = scores_for_chromosomes[-PARENTS_COUNT:]
		top_scores = [x[1] for x in top_performers]
		print("elite " + str(SELECTION_RATE) + ": " + "(min: " + str(min(top_scores)) + ", avg: " + str(mean(top_scores)) + ", max: " + str(max(top_scores)) + ")")
		chromosome = top_performers[-1][0]
		result = brainfuck.evaluate(chromosome)
		print("top: " + chromosome + ", result: " + result + ", score: " + str(self.fitness_string(result, self.target)))
		print("")
		return top_performers

	def generate_population(self, population):
		while len(population) < POPULATION:
			length = random.randint(PROGRAM_LENGTH_LOWER_BOUND, PROGRAM_LENGTH_UPPER_BOUND)
			chromosome = ""
			for i in range(0, length):
				chromosome += random.choice(AVAILABLE_OPS)
			if brainfuck.evaluate(chromosome) is not None: # We don't want programs that are syntactically incorrect
				population.append(chromosome)
		return population

	def pair(self, parents, softmax_parents, total_parents_score):
		pick_parent_a = random.uniform(0, total_parents_score)
		pick_parent_b = random.uniform(0, total_parents_score)
		return [self.roulette_selection(parents, softmax_parents, pick_parent_a), self.roulette_selection(parents, softmax_parents, pick_parent_b)]

	def generate_pairs(self, parents):
		softmax_parents = self.softmax([x[1] for x in parents])
		total_parents_score = sum(softmax_parents)
		pairs = []
		while len(pairs) != POPULATION:
			pair = self.pair(parents, softmax_parents, total_parents_score)
			if len(pair) == 2 and pair[0] is not None and pair[1] is not None:
				pairs.append(pair)
		return pairs

	def softmax(self, x):
		b = np.max(x)
		y = np.exp(x - b)
		return y / y.sum()

	def roulette_selection(self, parents, softmax_parents, pick):
		current = 0.0
		for i in range(0, len(parents)):
			current += softmax_parents[i]
			if current > pick:
				return parents[i]

	def fitness_string(self, input_string, target):
		fitness_score = 0
		for i, c in enumerate(input_string):
			input_score = ord(c)
			if len(target) > i:
				target_score = ord(target[i])
				fitness_score += ASCII_CHARS_COUNT-abs(input_score-target_score)
		length_diff = abs(len(target)-len(input_string))
		for _ in range(0, length_diff):
			fitness_score -= ASCII_CHARS_COUNT
		# print(repr(input_string))
		# print(len(input_string))
		# print(fitness_score)
		# exit()
		return fitness_score
	
if __name__ == "__main__":
	if len(sys.argv) == 2:
		MetaProgrammer(str(sys.argv[1]))
	else: 
		print("Usage:", sys.argv[0], "text to find")
	