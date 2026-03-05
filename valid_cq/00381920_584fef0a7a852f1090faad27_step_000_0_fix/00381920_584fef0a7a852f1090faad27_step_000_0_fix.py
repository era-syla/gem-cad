import cadquery as cq
from math import radians

# Parameters
base_length = 60
base_width = 40
base_height = 40

rack_length = 100
rack_width = 10
rack_thickness = 10
rack_angle = 20  # degrees

tooth_base = 6
tooth_height = 6
num_teeth = int(rack_length // tooth_base)

post_width = 6
post_depth = 6
post_height = 80
post_x = base_length * 0.25

# Base block
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Rack block (before rotation)
rack = (
    cq.Workplane("XY")
    .box(rack_length, rack_width, rack_thickness, centered=(False, True, False))
    .translate((0, 0, base_height))
    .rotate((0, 0, base_height), (0, 1, base_height), rack_angle)
)

# Start result with base and rack
result = base.union(rack)

# Create and union teeth
for i in range(num_teeth):
    x0 = i * tooth_base
    tooth = (
        cq.Workplane("XZ")
        .polyline([(0, 0), (tooth_base, 0), (tooth_base / 2, tooth_height)])
        .close()
        .extrude(rack_width)
        .translate((x0, -rack_width / 2, base_height + rack_thickness))
        .rotate((0, 0, base_height), (0, 1, base_height), rack_angle)
    )
    result = result.union(tooth)

# Vertical post
post = (
    cq.Workplane("XY")
    .box(post_width, post_depth, post_height, centered=(True, True, False))
    .translate((post_x, 0, base_height))
)
result = result.union(post)