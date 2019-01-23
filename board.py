import json


class Board:
    def __init__(self, board_name, units, board_outline, drilled_holes, placement, components):
        self.board_name = board_name
        self.units = units
        self.board_outline = board_outline
        self.drilled_holes = drilled_holes
        self.placement = placement
        self.components = components

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class BoardOutline:
    def __init__(self, outline_owner, thickness, points):
        self.outline_owner = outline_owner
        self.thickness = thickness
        self.points = points

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class DrilledHole:
    def __init__(self, diameter, x, y, plating_style, associated_part, hole_type, hole_owner):
        self.diameter = diameter
        self.x = x
        self.y = y
        self.plating_style = plating_style
        self.associated_part = associated_part
        self.hole_type = hole_type
        self.hole_owner = hole_owner

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Placement:
    def __init__(self, package_name, part_number, ref_defs, x, y, mounting_offset, rotation_angle_deg, side_of_board,
                 placement_status):
        self.package_name = package_name
        self.part_number = part_number
        self.ref_defs = ref_defs
        self.x = x
        self.y = y
        self.mounting_offset = mounting_offset
        self.rotation_angle_deg = rotation_angle_deg
        self.side_of_board = side_of_board
        self.placement_status = placement_status

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Component:
    def __init__(self, geometry_name, part_number, units, height, points):
        self.geometry_name = geometry_name
        self.part_number = part_number
        self.units = units
        self.height = height
        self.points = points

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Point:
    def __init__(self, loop_label, x, y, include_angle_deg):
        self.loop_label = loop_label
        self.x = x
        self.y = y
        self.include_angle_deg = include_angle_deg

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
