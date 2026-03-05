import cadquery as cq

# Parameters
thickness = 5
width = 150
depth = 100
cut_width = 80
cut_depth = 40
hole_dia = 6

# Create base plate
plate = cq.Workplane("XY").box(width, depth, thickness)

# Create U-shaped cutout
cut_offset_y = -(depth/2 - cut_depth/2)
cut = cq.Workplane("XY").transformed(offset=(0, cut_offset_y, 0)).box(cut_width, cut_depth, thickness)

# Subtract cutout to form U-shape
result = plate.cut(cut)

# Define hole positions on top face (Z+)
hole_positions = [
    (-50,  25),
    (-50, -25),
    ( 50,  25),
    ( 50, -25),
    (  0,  40),
    (-20, -10),
    (  0, -10),
    ( 20, -10),
]

# Drill holes through the plate
result = result.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_dia)