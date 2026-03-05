import cadquery as cq
import math

# Parameters
length = 120
width = 40
thickness = 6
corner_radius = 5

oval_length = 80
oval_width = 20
pocket_depth = 2

sq_w = 8
sq_h = 3
sq_sep = 20

boss_r = 15
boss_h = 5
boss_offset = length/2 - boss_r - 5

central_hole_dia = 6
bolt_hole_dia = 3
bolt_count = 8
bolt_circle_r = 12

# Base plate
result = cq.Workplane("XY").rect(length, width).extrude(thickness)

# Chamfer vertical edges
result = result.edges("|Z").chamfer(0.5)

# Oval pocket in center
result = result.faces(">Z").workplane().rect(oval_length, oval_width).cutBlind(-pocket_depth)

# Two small rectangular pockets inside the oval
for x in (-sq_sep/2, sq_sep/2):
    result = result.faces(">Z").workplane().center(x, 0).rect(sq_w, sq_h).cutBlind(-pocket_depth)

# Circular boss on one end
result = result.faces(">Z").workplane().center(boss_offset, 0).circle(boss_r).extrude(boss_h)

# Central hole through the boss
result = result.faces(">Z").workplane().center(boss_offset, 0).hole(central_hole_dia)

# Bolt hole pattern around the boss
bolt_pts = [
    (math.cos(2*math.pi*i/bolt_count)*bolt_circle_r, math.sin(2*math.pi*i/bolt_count)*bolt_circle_r)
    for i in range(bolt_count)
]
result = result.faces(">Z").workplane().center(boss_offset, 0).pushPoints(bolt_pts).hole(bolt_hole_dia)