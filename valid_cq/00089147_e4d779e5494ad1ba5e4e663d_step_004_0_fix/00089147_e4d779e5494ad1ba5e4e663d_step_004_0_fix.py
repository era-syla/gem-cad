import cadquery as cq

# Parameters
rod_radius = 1.5
rod_spacing = 6.0
short_length = 60.0
long_length = 120.0
group_offset = 15.0

# Compute point lists for the two sets of 4 rods
tall_points = [
    (group_offset + x, y)
    for x in (-rod_spacing / 2, rod_spacing / 2)
    for y in (-rod_spacing / 2, rod_spacing / 2)
]
short_points = [
    (-group_offset + x, y)
    for x in (-rod_spacing / 2, rod_spacing / 2)
    for y in (-rod_spacing / 2, rod_spacing / 2)
]

# Build the model
result = (
    cq.Workplane("XY")
    .pushPoints(tall_points)
    .cylinder(long_length, rod_radius)
    .pushPoints(short_points)
    .cylinder(short_length, rod_radius)
)