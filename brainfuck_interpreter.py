
import sys

OPERATIONS_LIMIT = 10000 # necessary to prevent halting

def execute(filename):
    f = open(filename, "r")
    result = evaluate(f.read())
    print(result)
    f.close()

def evaluate(code):
    code = cleanup(code)
    return run(code)

def set_cell_value(value, cells, cell_ptr):
    cells[cell_ptr] += value
    if cells[cell_ptr] > 255:
        cells[cell_ptr] = 0
    elif cells[cell_ptr] < 0:
        cells[cell_ptr] = 255
    return cells, cell_ptr

def cleanup(code):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def is_index_in_collection(index, collection):
    return True if index < len(collection) and index >= 0 else False

def pair_brackets(code):
    open_bracket_indexes = []
    close_bracket_indexes = []
    stack = []
    open_brackets = 0
    close_brackets = 0
    for index, command in enumerate(code):
        if command == '[':
            open_brackets += 1
            stack.append(index)
        elif command == ']':
            close_brackets += 1
            if len(stack) > 0:
                open_bracket_indexes.append(stack.pop())
                close_bracket_indexes.append(index)
            else:
                return None
    if open_brackets != close_brackets:
        return None
    return open_bracket_indexes, close_bracket_indexes

def run(code):
    operations = 0
    cells = [0]
    cell_ptr = 0
    src_ptr = 0
    result = ""

    brackets = pair_brackets(code)
    if not brackets:
        #print("No brackets")
        return None
    open_bracket_indexes = brackets[0]
    close_bracket_indexes = brackets[1]

    while src_ptr < len(code):
        if operations >= OPERATIONS_LIMIT:
            #print("halt!")
            return None

        command = code[src_ptr]

        if command == '+':
            if not is_index_in_collection(cell_ptr, cells):
                #print("cell_ptr not in cells for +")
                return None 
            cells, cell_ptr = set_cell_value(1, cells, cell_ptr)

        elif command == '-':
            if not is_index_in_collection(cell_ptr, cells):
                #print("cell_ptr not in cells for -")
                return None
            cells, cell_ptr = set_cell_value(-1, cells, cell_ptr)

        elif command == '<':
            cell_ptr -= 1

        elif command == '>':
            cell_ptr += 1
            if cell_ptr > len(cells)-1:
                cells.append(0)

        elif command == '[' or command == ']':
            if not is_index_in_collection(cell_ptr, cells):
                #print("cell_ptr not in cells for [ or ]")
                return None
            if command == '[' and cells[cell_ptr] == 0:
                index = open_bracket_indexes.index(src_ptr)
                src_ptr =  close_bracket_indexes[index]
            elif command == ']' and cells[cell_ptr] != 0:
                index = close_bracket_indexes.index(src_ptr)
                src_ptr = open_bracket_indexes[index]

        elif command == ',':
            return None # No inputs as for now

        elif command == '.':
            if not is_index_in_collection(cell_ptr, cells):
                #print("cell_ptr not in cells for .")
                return None
            new_char = chr(cells[cell_ptr])
            result += new_char

        src_ptr += 1
        operations += 1
    return result

if __name__ == '__main__':
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else: 
        print("Usage: python3 ", sys.argv[0], " <filename>")
