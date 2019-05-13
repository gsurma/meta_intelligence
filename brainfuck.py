#!/usr/bin/python

# > 	Increment the pointer.
# < 	Decrement the pointer.
# + 	Increment the byte at the pointer.
# - 	Decrement the byte at the pointer.
# . 	Output the byte at the pointer.
# , 	Input a byte and store it in the byte at the pointer.
# [ 	Jump forward past the matching ] if the byte at the pointer is zero.
# ] 	Jump backward to the matching [ unless the byte at the pointer is zero.

#
# Brainfuck Interpreter
#

import sys

OPERATIONS_LIMIT = 1000 # Necessary to prevent halting
CELLS = 30000


def execute(filename):
	f = open(filename, "r")
	evaluate(f.read())
	f.close()

def evaluate(code):
	code = cleanup(list(code))
	bracemap = build_bracemap(code)

	cells, codeptr, cellptr = [0], 0, 0
	result = ""
	operations = 0

	if bracemap is None:
		return None

	while codeptr < len(code):
		if operations >= OPERATIONS_LIMIT:
			return None
		command = code[codeptr]

		if command == ">":
			cellptr += 1
			if len(cells) <= cellptr:
				cells.append(0)
			# if cellptr == len(cells):
		 #   		cells.append(0)

		if command == "<":
			cellptr = 0 if cellptr <= 0 else cellptr - 1

		# if command == "+":
		# 	cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < CELLS else 0

		# if command == "-":
		# 	cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else CELLS

		if command == "+":
			cells[cellptr] = cells[cellptr] + 1 

		if command == "-":
			cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 0

		if command == "[" and cells[cellptr] == 0:
			if codeptr not in bracemap:
				return None
			else:
				codeptr = bracemap[codeptr]

		if command == "]" and cells[cellptr] != 0:
			if codeptr not in bracemap:
				return None
			else:
				codeptr = bracemap[codeptr]

		if command == ".":
			result += chr(cells[cellptr])

		if command == ",":
			return None # we don't accept additional inputs, let's skip

		codeptr += 1
		operations += 1
	return result

def cleanup(code):
	return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def build_bracemap(code):
	temp_bracestack, bracemap = [], {}
	braces_count = 0
	for position, command in enumerate(code):
		if command == "[":
			braces_count += 1
			temp_bracestack.append(position)
		if command == "]":
			braces_count += 1
			if len(temp_bracestack) > 0:
				start = temp_bracestack.pop()
				bracemap[start] = position
				bracemap[position] = start
			else:
				return None
	# print(bracemap)
	# print(braces_count)
	# TODO: fix
	#https://gist.github.com/unnikked/cfad836abd9e4619a1b1
	#https://github.com/praharshjain/brainfuck-interpreter/blob/master/brainfuck_interpreter.py
	#https://codereview.stackexchange.com/questions/134578/a-brainfuck-interpreter-in-python-3
	if braces_count != len(bracemap):
		return None
	return bracemap

if __name__ == "__main__":
	if len(sys.argv) == 2:
		execute(sys.argv[1])
	else: 
		print("Usage:", sys.argv[0], "filename")

