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

PROGRAM_LENGTH_LOWER_BOUND = 10
PROGRAM_LENGTH_UPPER_BOUND = 100
MAX_EPISODES = 10000
OUTPUT_DIR = "./output/"

class ReinforcementLearningMetaProgrammer():

	target = ""
	episode = 0
	max_fitness_score = 0
	start_time = None
	best_fitness_scores = []

	def __init__(self, target):
		self.target = target
		self.max_fitness_score = len(self.target)*ASCII_CHARS_COUNT
		self.start_time = time.time()

		print("Started looking for: " + repr(target))
		self.reinforcement_learning()

	def reinforcement_learning(self):
		while episode < MAX_EPISODES:
    		episode += 1
    		state = env.reset()
    		state_n = [np.reshape(i, [1, state_shape_size]) for i in state]
    		episode_agent_rewards = [0 for _ in range(len(agents))]
    		total_reward = step = 0
    		gameover = False
    		episode_untagged = []
    		start_time = time.time()

		    while not gameover:
		        step += 1
		        action_n = [agent.get_action(state) for agent, state in zip(agents, state_n)]
		        reward, next_state, done, untagged_ratio = env.step(action_n)
		        next_state = [np.reshape(i, [1, state_shape_size]) for i in next_state]
		        for i in range(len(agents)):
		            episode_agent_rewards[i] += reward[i]
		        total_reward += sum(reward)
		        episode_untagged.append(untagged_ratio)

		        if episode % RENDERING_FREQUENCY == 0:
		            render_env_image(env, episode, step)

		        async def train_agent(i):
		            agents[i].train_model(action_n[i], state_n[i], next_state[i], reward[i], done)

		        async def train_all_agents():
		            await asyncio.gather(*(train_agent(i) for i in range(len(agents))))

		        results = loop.run_until_complete(train_all_agents())
		           
		        state_n = next_state
		        terminal = (step >= MAX_EPIOSDE_LENGTH)
		        if done or terminal:
		            gameover = True

		    if episode % TARGET_MODEL_UPDATE_FREQUENCY == 0:
		        [agent.update_target_model() for agent in agents]


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
		ReinforcementLearningnMetaProgrammer(str(sys.argv[1]))
	else: 
		print("Usage: python3 ", sys.argv[0], " <text_to_find>")
	