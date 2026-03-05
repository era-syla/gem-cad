import cadquery as cq
import math

# Parameters
N_teeth = 36
thickness = 5.0
R_outer = 90.0
tooth_height = 8.0
R_inner = 50.0

# Base ring without teeth
result = (
    cq.Workplane("XY")
    .circle(R_outer - tooth_height)
    .circle(R_inner)
    .extrude(thickness)
)

# Tooth profile
pitch_radius = R_outer - tooth_height/2
tooth_pitch = 2 * math.pi * pitch_radius / N_teeth
tooth_width = tooth_pitch * 0.7

tooth = (
    cq.Workplane("XY")
    .rect(tooth_width, tooth_height)
    .extrude(thickness)
    .translate((0, R_outer - tooth_height/2, 0))
)

# Add teeth around the ring
for i in range(N_teeth):
    angle = 360.0 * i / N_teeth
    result = result.union(tooth.rotate((0, 0, 0), (0, 0, 1), angle))

# Cut circular mounting holes
hole_count = 6
hole_radius = (R_outer - tooth_height + R_inner) / 2
hole_diameter = 8.0
hole_angles = [i * 360.0 / hole_count for i in range(hole_count)]
hole_points = [
    (hole_radius * math.cos(math.radians(a)), hole_radius * math.sin(math.radians(a)))
    for a in hole_angles
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

# Cut rectangular pockets for weight reduction
pocket_count = 6
pocket_radius = (R_inner + (R_outer - tooth_height)) / 2 - 8.0
pocket_width = 6.0
pocket_length = 30.0
pocket_angles = [i * 360.0 / pocket_count + 360.0 / (2 * pocket_count) for i in range(pocket_count)]
pocket_points = [
    (pocket_radius * math.cos(math.radians(a)), pocket_radius * math.sin(math.radians(a)))
    for a in pocket_angles
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pocket_points)
    .rect(pocket_width, pocket_length)
    .cutThruAll()
)

# Fillet all horizontal edges for a smooth finish
result = result.edges("|Z").fillet(1.0)