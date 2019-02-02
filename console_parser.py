import sys

from parser import read_board, read_components


def print_instruction():
    print("Simple board and component file parser into json. Usage:\r\n\r\n"
          "python3 parser.py <component_file> <board_file>\r\n\r\n"
          "output can be streamed into a file manually.")

if len(sys.argv) != 3:
    print_instruction()
    exit()

components_file = sys.argv[1]
components_lines = [line.rstrip('\n') for line in open(components_file)]
board_file = sys.argv[2]
board_lines = [line.rstrip('\n') for line in open(board_file)]

components = read_components(components_lines)
component_board = read_board(board_lines, components)
print(component_board.to_json())
