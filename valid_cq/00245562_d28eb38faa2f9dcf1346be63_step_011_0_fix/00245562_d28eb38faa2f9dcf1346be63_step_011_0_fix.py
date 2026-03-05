import cadquery as cq

# Parameters
plate_size = 60
plate_thickness = 8
corner_radius = 5
slot_width = 4
slot_length = plate_size * 1.5
central_hole_diameter = 12
side_hole_diameter = 6
pocket_depth = 4

# Base plate with rounded corners
result = cq.Workplane("XY") \
    .rect(plate_size, plate_size) \
    .extrude(plate_thickness) \
    .edges("|Z").fillet(corner_radius)

# Diagonal through slots
result = result.faces(">Z").workplane() \
    .transformed(rotate=(0, 0, 45)).rect(slot_length, slot_width).cutThruAll() \
    .faces(">Z").workplane() \
    .transformed(rotate=(0, 0, 135)).rect(slot_length, slot_width).cutThruAll()

# L-shaped pocket (shallow)
# vertical leg of L
v_x = plate_size * 0.25
v_y = -plate_size * 0.25
result = result.faces(">Z").workplane() \
    .pushPoints([(v_x, v_y)]) \
    .rect(slot_width, plate_size * 0.5).cutBlind(pocket_depth)
# horizontal leg of L
h_x = v_x + (plate_size * 0.25)
h_y = 0
result = result.faces(">Z").workplane() \
    .pushPoints([(h_x, h_y)]) \
    .rect(plate_size * 0.25, slot_width).cutBlind(pocket_depth)

# Central through hole
result = result.faces(">Z").workplane().hole(central_hole_diameter)

# Side through hole
result = result.faces(">X").workplane().hole(side_hole_diameter)