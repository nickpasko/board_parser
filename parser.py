import sys
import board


def read_components(lines):
    components = []
    components_start = 0
    for i in range(0, len(lines) - 1):
        if i < len(lines) and lines[i] == 'END_HEADER':
            components_start = i + 1
            break

    for i in range(components_start, len(lines) - 1):
        if i < len(lines) and lines[i] == '.ELECTRICAL':
            i += 1
            geometry_name, part_number, units, height = lines[i].split()
            points = []
            i += 1
            while lines[i] != '.END_ELECTRICAL':
                loop_label, x, y, include_angle_deg = lines[i].split()
                points.append(board.Point(loop_label, x, y, include_angle_deg))
                i += 1
            components.append(board.Component(geometry_name.replace('\"', ''), part_number.replace('\"', ''), units, height, points))

    return components


def read_board(lines, components):
    i = 0
    while i < len(lines) and lines[i] != '.END_HEADER':
        i += 1
    board_name, units = lines[i - 1].split()
    while i < len(lines) and not lines[i].startswith('.BOARD_OUTLINE'):
        i += 1
    outline_owner = lines[i].split()[1]
    i += 1
    outline_thickness = lines[i]
    i += 1
    points = []
    while i < len(lines) and lines[i] != '.END_BOARD_OUTLINE':
        loop_label, x, y, include_angle_deg = lines[i].split()
        points.append(board.Point(loop_label, x, y, include_angle_deg))
        i += 1
    board_outline = board.BoardOutline(outline_owner, outline_thickness, points)
    while i < len(lines) and lines[i] != '.DRILLED_HOLES':
        i += 1
    i += 1
    drilled_holes = []
    while i < len(lines) and lines[i] != '.END_DRILLED_HOLES':
        diameter, x, y, plating_style, associated_part, hole_type, hole_owner = lines[i].split()
        drilled_holes.append(board.DrilledHole(diameter, x, y, plating_style, associated_part, hole_type, hole_owner))
        i += 1
    i += 2
    placement = []
    while i < len(lines) and lines[i] != ".END_PLACEMENT":
        package_name, part_number, ref_defs = lines[i].split()
        x, y, mounting_offset, rotation_angle_deg, side_of_board, placement_status = lines[i + 1].split()
        placement.append(board.Placement(package_name.replace('\"', ''), part_number.replace('\"', ''), ref_defs.replace('\"', ''),
                                         x, y, mounting_offset, rotation_angle_deg, side_of_board, placement_status))
        i += 2
    return board.Board(board_name, units, board_outline, drilled_holes, placement, components)


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
