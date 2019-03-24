import board


def read_geometries(lines):
    component_geometries = []
    geometries_start = 0
    for i in range(0, len(lines) - 1):
        if i < len(lines) and lines[i] == 'END_HEADER':
            geometries_start = i + 1
            break

    for i in range(geometries_start, len(lines) - 1):
        if i < len(lines) and lines[i] == '.ELECTRICAL':
            i += 1
            package_name, part_number, units, height = lines[i].split()
            points = []
            i += 1
            while lines[i] != '.END_ELECTRICAL':
                loop_label, x, y, include_angle_deg = lines[i].split()
                points.append(board.Point(loop_label, x, y, include_angle_deg))
                i += 1
            component_geometries.append(board.ComponentGeometry(package_name.replace('\"', ''), part_number.replace('\"', ''), units, height, points))

    return component_geometries


def read_board(lines, component_geometries):
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
    components = []
    while i < len(lines) and lines[i] != ".END_PLACEMENT":
        package_name, part_number, ref_defs = lines[i].split()
        x, y, mounting_offset, rotation_angle_deg, side_of_board, placement_status = lines[i + 1].split()
        components.append(board.Component(package_name.replace('\"', ''), part_number.replace('\"', ''), ref_defs.replace('\"', ''),
                                         x, y, mounting_offset, rotation_angle_deg, side_of_board, placement_status))
        i += 2
    return board.Board(board_name.replace('\"', ''), units, board_outline, drilled_holes, components, component_geometries)