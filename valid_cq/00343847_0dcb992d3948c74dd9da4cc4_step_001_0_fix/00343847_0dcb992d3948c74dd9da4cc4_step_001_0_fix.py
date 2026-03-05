import cadquery as cq
import math

# Bracket parameters
plate_thickness = 5
plate_height = 40
base_length = 60
extrude_depth = 10

# Bracket profile in XZ plane (including gusset)
profile = [
    (0, 0),
    (base_length, 0),
    (base_length, plate_thickness),
    (10, plate_thickness),
    (10, 35),
    (5, plate_height),
    (0, plate_height),
]

# Build bracket
bracket = cq.Workplane("XZ").polyline(profile).close().extrude(extrude_depth)

# Holes in vertical face (Y positive)
vholes = [(30, 20), (20, 30), (40, 30)]
bracket = bracket.faces(">Y").workplane().hole(10) \
    .pushPoints(vholes).hole(5)

# Hole through base (bottom face, Z negative)
bracket = bracket.faces("<Z").workplane().pushPoints([(40, 5)]).hole(8)

# Cylinder flange parameters
cyl_radius = 15
cyl_height = 10
ring_hole_radius = 10
ring_hole_dia = 3
ring_holes = 8

# Build flange
cyl = cq.Workplane("XY").circle(cyl_radius).extrude(cyl_height)
# Central counterbore/pocket
cyl = cyl.faces(">Z").workplane().hole(10)
# Ring of small holes
angles = [i * 360 / ring_holes for i in range(ring_holes)]
points = [(math.cos(math.radians(a)) * ring_hole_radius,
           math.sin(math.radians(a)) * ring_hole_radius)
          for a in angles]
cyl = cyl.faces(">Z").workplane().pushPoints(points).hole(ring_hole_dia)
# Position flange beside bracket
cyl = cyl.translate((80, 5, 0))

# Combine parts
result = bracket.union(cyl)