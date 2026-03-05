import cadquery as cq
import math

# Key dimensions
shaft_radius = 3
shaft_height = 40
torus_major_radius = 12
torus_minor_radius = 5
bow_center_z = shaft_height + torus_minor_radius

# Create the shaft (cylindrical rod)
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_height)
)

# Create the torus (donut/bow of the key) at the top of the shaft
# Torus: revolve a circle around the Z axis
torus = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(torus_major_radius, 0, bow_center_z))
    .circle(torus_minor_radius)
    .revolve(360, axisStart=(- torus_major_radius, 0, 0), axisEnd=(-torus_major_radius, 0, 1))
)

# Create the key head/bit (rectangular block at the bottom)
# Square bit extending to the side
bit_width = 8
bit_height = 6
bit_depth = 8

bit = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(bit_width / 2, 0, -bit_height / 2))
    .box(bit_width, bit_depth, bit_height)
)

# Small square notch/tooth on the bit
tooth_width = 4
tooth_height = 4
tooth_depth = bit_depth

tooth = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(bit_width + tooth_width / 2, 0, -bit_height / 2))
    .box(tooth_width, tooth_depth, tooth_height)
)

# Combine all parts
result = shaft.union(torus).union(bit).union(tooth)