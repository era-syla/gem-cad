import cadquery as cq
from math import sin, cos, radians

# Parameters
disc_dia = 60
disc_th = 8
boss_dia = 20
boss_h = 3
pocket_rad = 12
pocket_depth = 1
slot_width = 6
slot_depth = 2
hole_dia = 4

# Derived
slot_length = disc_dia/2 - pocket_rad
hole_rad = disc_dia/2 - 6

# Base disc
result = cq.Workplane("XY").circle(disc_dia/2).extrude(disc_th)

# Shallow central pocket
result = result.faces(">Z").workplane().circle(pocket_rad).cutBlind(-pocket_depth)

# Radial slots (shallow)
wp = result.faces(">Z").workplane()
for i in range(3):
    angle = i * 120
    r_center = pocket_rad + slot_length/2
    x = r_center * cos(radians(angle))
    y = r_center * sin(radians(angle))
    wp = wp.pushPoints([(x, y)]).slot2D(slot_length, slot_width, angle)
result = wp.cutBlind(-slot_depth)

# Small through-holes near rim
wp2 = result.faces(">Z").workplane()
pts = []
for i in range(3):
    angle = i * 120 + 60
    x = hole_rad * cos(radians(angle))
    y = hole_rad * sin(radians(angle))
    pts.append((x, y))
wp2 = wp2.pushPoints(pts).circle(hole_dia/2)
result = wp2.cutThruAll()

# Central boss
result = result.faces(">Z").workplane().circle(boss_dia/2).extrude(boss_h)