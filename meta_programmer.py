# > 	Increment the pointer.
# < 	Decrement the pointer.
# + 	Increment the byte at the pointer.
# - 	Decrement the byte at the pointer.
# . 	Output the byte at the pointer.
# , 	Input a byte and store it in the byte at the pointer.
# [ 	Jump forward past the matching ] if the byte at the pointer is zero.
# ] 	Jump backward to the matching [ unless the byte at the pointer is zero.

# /// Default constructor sets mutation rate to 5%, crossover to 80%, population to 100,
# 		/// and generations to 2000.

#fitness += 256 - Math.Abs(console[i] - targetString[i]);

import brainfuck

result = brainfuck.evaluate("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++")
print(result)

def fitness(input, target):
	fitness_score = 0
	for i, c in enumerate(input):
		input_score = ord(c)
		if len(target) > i:
			target_score = ord(target[i])
			score = 256-abs(input_score-target_score)
		else:
			score = -1
		fitness_score += score
	return fitness_score

		
input = "Hello"
target = "Hello"

score = fitness(input, target)
print("final", score)

