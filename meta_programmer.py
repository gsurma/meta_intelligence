# > 	Increment the pointer.
# < 	Decrement the pointer.
# + 	Increment the byte at the pointer.
# - 	Decrement the byte at the pointer.
# . 	Output the byte at the pointer.
# , 	Input a byte and store it in the byte at the pointer.
# [ 	Jump forward past the matching ] if the byte at the pointer is zero.
# ] 	Jump backward to the matching [ unless the byte at the pointer is zero.

# https://copy.sh/brainfuck/text.html

import brainfuck
import random
import copy
import numpy as np
from statistics import mean

ASCII_CHARS_COUNT = 256
POPULATION = 1000
MUTATION_RATE = 0.01
SELECTION_RATE = 0.8
PARENTS_COUNT = int(POPULATION * SELECTION_RATE)

PROGRAM_LENGTH_LOWER_BOUND = 10
PROGRAM_LENGTH_UPPER_BOUND = 100

AVAILABLE_OPS = [">", "<", "+", "-", ".", ",", "[", "]"]


class MetaProgrammer():

	target = ""
	generation = 0

	def __init__(self, target):
		self.target = target

		#chromosome = "+[----->+++<]>+.+." #hi
		# chromosome = "]]-+,--><.,[>" #478
		# result = brainfuck.evaluate(chromosome)
		# print(len(chromosome))
		# print(result)
		# score = self.fitness_string(chromosome, self.target)
		# print(score)
		# exit()

		self.genetic_evolution()


	def genetic_evolution(self):
		population = self.generate_initial_population()
		while self.should_keep_evolving(population):
			print("generation: " + str(self.generation) + ", population: " + str(len(population)) + ", mutation_rate: " + str(MUTATION_RATE))

			# 1. Selection
			parents = self.strongest_parents(population)

			# 2. Crossover (Roulette selection)
			pairs = []
			while len(pairs) != POPULATION:
			    pairs.append(self.pair(parents))

			base_offsprings = []
			for pair in pairs:
				offsprings = self.crossover(pair[0][0], pair[1][0])
				base_offsprings.append(offsprings[0])

			# # 3. Mutation
			new_population = self.mutation(base_offsprings)
			population = new_population
			self.generation += 1

	def should_keep_evolving(self, population):
		for chromosome in population:
			result = brainfuck.evaluate(chromosome)
			print("chromosome: " + chromosome + ", result: " + result + ", score: " + str(self.fitness_string(chromosome, self.target)))
			if result == self.target:
				print("FOUND SOLUTION: " + chromosome + " for: " + target)
				return False
		return True

	def mutation(self, base_offsprings):
		offsprings = []
		for offspring in base_offsprings:
			offspring_mutation = copy.deepcopy(offspring)
			for i in range(0, len(offspring_mutation)):
				if np.random.choice([True, False], p=[MUTATION_RATE, 1-MUTATION_RATE]):
					offspring_mutation = self.set_value_at_index(offspring_mutation, random.choice(AVAILABLE_OPS), i)
					# print("before: ", offspring)
					# print("after: ", offspring_mutation)
					# exit()
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
			return ""

	def set_value_at_index(self, string, value, i):
		if i > len(string):
			return string + value # TODO: maybe just pass?
		else:
			return string[:i] + value + string[i+1:]

	def strongest_parents(self, population):
		scores_for_chromosomes = []
		for i in range(0, len(population)):
			chromosome = population[i]
			scores_for_chromosomes.append((chromosome, self.fitness_string(chromosome, self.target)))
		scores_for_chromosomes.sort(key=lambda x: x[1])
		print("population: " + str(mean([x[1] for x in scores_for_chromosomes])))

		top_performers = scores_for_chromosomes[-PARENTS_COUNT:]
		top_scores = [x[1] for x in top_performers]
		print("top " + str(SELECTION_RATE) + ": " + "(min: " + str(min(top_scores)) + ", avg: " + str(mean(top_scores)) + ", max: " + str(max(top_scores)) + ")")
		print("")
		return top_performers

	def generate_initial_population(self):
		population = []
		while len(population) < POPULATION:
			length = random.randint(1, PROGRAM_LENGTH_UPPER_BOUND)
			chromosome = ""
			for i in range(0, length):
				chromosome += random.choice(AVAILABLE_OPS)
			if brainfuck.evaluate(chromosome) != "": # We don't want programs that are syntactically incorrect
				population.append(chromosome)
		return population

	def pair(self, parents):
		total_parents_score = sum([x[1] for x in parents])
		pick_parent_a = random.uniform(0, total_parents_score)
		pick_parent_b = random.uniform(0, total_parents_score)
		return [self.roulette_selection(parents, pick_parent_a), self.roulette_selection(parents, pick_parent_b)]

	def roulette_selection(self, parents, pick):
		current = 0
		for parent in parents:
			current += parent[1]
			if current > pick:
				return parent

	def fitness_string(self, input, target):
		fitness_score = 0
		for i, c in enumerate(input):
			input_score = ord(c)
			if len(target) > i:
				target_score = ord(target[i])
				score = ASCII_CHARS_COUNT-abs(input_score-target_score)
			else:
				score = -1
			fitness_score += score
		return fitness_score	

def main():
	MetaProgrammer("hi")

if __name__ == "__main__":
	main()