import cadquery as cq
import math

# Parameters
plate_edge_to_edge = 200
plate_thickness = 5
hex_hole_side = 8
boss_height = 3
pocket_size = 10

# Derived spacings for hex grid
x_spacing = 1.5 * hex_hole_side
y_spacing = math.sqrt(3) * hex_hole_side

# Create the main hexagonal plate
plate = cq.Workplane("XY") \
    .polygon(6, plate_edge_to_edge) \
    .extrude(plate_thickness)

# Cut out a ring of hexagonal holes at axial distance = 2
ring = 2
hole_positions = []
for q in range(-ring, ring + 1):
    for r in range(-ring, ring + 1):
        if abs(q + r) <= ring and max(abs(q), abs(r), abs(-q - r)) == ring:
            hole_positions.append((q, r))

for q, r in hole_positions:
    x = x_spacing * q
    y = y_spacing * (r + q / 2)
    plate = plate.workplane(offset=0) \
        .transformed(offset=(x, y, 0)) \
        .polygon(6, 2 * hex_hole_side) \
        .cutThruAll()

# Add three central hex bosses at axial coords (0,0), (1,-1), (-1,1)
central_positions = [(0, 0), (1, -1), (-1, 1)]
for q, r in central_positions:
    x = x_spacing * q
    y = y_spacing * (r + q / 2)
    plate = plate.workplane(offset=plate_thickness) \
        .transformed(offset=(x, y, 0)) \
        .polygon(6, 2 * hex_hole_side) \
        .extrude(boss_height)

# Cut diamond-shaped pockets at the six plate vertices
radius = plate_edge_to_edge / 2 - pocket_size
for i in range(6):
    angle_deg = 60 * i + 30
    angle = math.radians(angle_deg)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    plate = plate.workplane(offset=plate_thickness - 0.1) \
        .transformed(offset=(x, y, 0), rotate=(0, 0, angle_deg)) \
        .polygon(4, pocket_size) \
        .cutThruAll()

# Create a small rectangular bar part
bar = cq.Workplane("XY") \
    .box(20, 5, 5) \
    .translate((-plate_edge_to_edge / 2 + 20, plate_edge_to_edge / 2 - 10, plate_thickness + 1))

# Create a small disc part
disc = cq.Workplane("XY") \
    .circle(8) \
    .extrude(3) \
    .translate((0, plate_edge_to_edge / 2 - 15, plate_thickness + 1))

# Create a tri-arm peg part
tri = cq.Workplane("XY")
for i in range(3):
    tri = tri.union(
        cq.Workplane("XY")
        .circle(2)
        .extrude(10)
        .rotate((0, 0, 0), (0, 0, 1), i * 120)
    )
tri = tri.translate((plate_edge_to_edge / 2 - 15, -plate_edge_to_edge / 2 + 15, plate_thickness + 1))

# Combine everything into the final result
result = plate.union(bar).union(disc).union(tri)