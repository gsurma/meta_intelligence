<h3 align="center">
  <img src="assets/meta_intelligence_icon_web.png" width="300">
</h3>

# Meta Intelligence

AI research environment for artificial code generation ([metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming)).


Check out corresponding Medium article: [Meta Intelligence - Writing Programs That Write Programs (Part 1: Genetic Evolution)](https://towardsdatascience.com/meta-intelligence-writing-programs-that-write-programs-part-1-genetic-evolution-679b65c37c5f)

## About
**Given an esoteric and minimalistic, though [Turing complete](https://en.wikipedia.org/wiki/Turing_completeness) programming language [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck), we aim to artificially generate programs that perform specific tasks.**

Brainfuck has only 8 instructions making it very easy to read for computers (check python interpreter `brainfuck_interpreter.py`) but on the other hand, very hard to understand for humans, thus the name.

	">" Increment the pointer.
	"<" Decrement the pointer.
	"+" Increment the byte at the pointer.
	"-" Decrement the byte at the pointer.
	"." Output the byte at the pointer.
	"[" Jump forward past the matching ] if the byte at the pointer is zero.
	"]"] Jump backward to the matching [ unless the byte at the pointer is zero.
	"," Input a byte and store it in the byte at the pointer.



### Genetic Evolution

Our goal is to generate a brainfuck program that outputs a given target string. Example usage for a target string of 'HI': `python3 genetic_evolution_meta_programmer.py 'HI'` 

0. We are going to start with a **population of random chromosomes** where every chromosome will be a brainfuck program represented as a string of random instructions. Example chromosome: `[->+]+.-><>+`. Keep in mind that the vast majority of randomly generated programs will be syntactically incorrect so we need to validate them with interpreter before adding to the population.
1. Then we are going to proceed to the **selection** phase where we are going to pick top performing programs. Programs are evaluated with a fitness function that calculates score for every character with the following function: `fitness_score += ASCII_CHARS_COUNT-abs(input_score-target_score)` which is basically calculating the distance from the given character to the desired one on the ASCII table. The closer we are to the target character. The bigger the score, the closer we are to our target with `ASCII_CHARS_COUNT` as a max per character. Maximum fitness score per chromosome is calculated as `len(self.target)*ASCII_CHARS_COUNT`.
2. Next we are going to **pair chromosomes** with roulette selection and perform a **crossover**.
3. Finally we are going to perform **mutation**. Some programs after mutation are invalid so we are going to replace them with the random valid ones to keep the population constant in size.
4. We are going to repeat steps 1-3 until we find the target string.

#### Hyperparameters

	POPULATION = 100
	MUTATION_RATE = 0.115
	MAX_MUTATION_ATTEMPTS = 500
	SELECTION_RATE = 0.9
	PROGRAM_LENGTH_LOWER_BOUND = 10
	PROGRAM_LENGTH_UPPER_BOUND = 100

#### Results
<img src="output/'!'.png">

	FOUND SOLUTION: +++++++++++++++++++++++++++++++++. for: '!' in: 5 minutes

---
	
<img src="output/'HI'.png">
	
	FOUND SOLUTION: ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+. for: 'HI'  in: 27 minutes

---
<img src="output/'123'.png">
	
	FOUND SOLUTION: +++++-+++[>+++++++<-]>-+.+.+. for: '123' in: 20 minutes


### Reinforcement Learning
Coming soon!

## Author

**Greg (Grzegorz) Surma**

[**PORTFOLIO**](https://gsurma.github.io)

[**GITHUB**](https://github.com/gsurma)

[**BLOG**](https://medium.com/@gsurma)

