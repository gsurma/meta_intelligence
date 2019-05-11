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
from statistics import mean

ASCII_CHARS_COUNT = 256
CROSSOVER = 0.8
POPULATION = 1000
MUTATION_RATE = 0.05
SELECTION_RATE = 0.1
PARENTS_COUNT = int(POPULATION * SELECTION_RATE)

PROGRAM_LENGTH_LOWER_BOUND = 10
PROGRAM_LENGTH_UPPER_BOUND = 100

AVAILABLE_OPS = [">", "<", "+", "-", ".", ",", "[", "]"]


class MetaProgrammer():

	target = ""
	generation = 0

	def __init__(self, target):
		self.target = target

		result = brainfuck.evaluate("+[----->+++<]>+.+.")
		print(result)

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
			exit()

			base_offsprings = []
			for pair in pairs:
				offsprings = self.crossover(pair[0][0], pair[1][0])
				base_offsprings.append(offsprings[-1])

			# # 3. Mutation
			# new_population = self.mutation(base_offsprings)
			# population = new_population
			self.generation += 1

	def should_keep_evolving(self, population):
		for chromosome in population:
			print(chromosome)
			result = brainfuck.evaluate(chromosome)
			print("result: ", result)
			if result == self.target:
				print("FOUND SOLUTION: " + chromosome + " for: " + target)
				return False
		return True

	# def mutation(self, base_offsprings):
	# 	offsprings = []
	# 	for offspring in base_offsprings:
	# 		offspring_mutation = copy.deepcopy(offspring)
	# 		for i in
	# 		for i in range(0, Constants.MODEL_FEATURE_COUNT):

	# 			for j in range(0, self.model.hidden_node_neurons):
	# 				if np.random.choice([True, False], p=[MUTATION_RATE, 1-MUTATION_RATE]):
	# 					offspring_mutation[i][j] = random.uniform(-1, 1)
	# 					offsprings.append(offspring_mutation)
	# 	return offsprings

	def crossover(self, x, y):
		offspring_x = x
		offspring_y = y
		for i in range(0, Constants.MODEL_FEATURE_COUNT):
			for j in range(0, self.model.hidden_node_neurons):
				if random.choice([True, False]):
					offspring_x[i][j] = y[i][j]
					offspring_y[i][j] = x[i][j]
		return offspring_x, offspring_y

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
		for i in range(0, POPULATION):
			length = random.randint(1, PROGRAM_LENGTH_UPPER_BOUND)
			gene = ""
			for j in range(0, length):
				gene += random.choice(AVAILABLE_OPS)
			population.append(gene)
		return population

	def pair(self, parents):
		total_parents_score = sum([x[1] for x in parents])
		pick = random.uniform(0, total_parents_score)
		return [self.roulette_selection(parents, pick), self.roulette_selection(parents, pick)]

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