import cadquery as cq
import math

num_teeth = 18
module = 2.0
pitch_dia = num_teeth * module
pitch_r = pitch_dia / 2
addendum = module
dedendum = 1.25 * module
outer_r = pitch_r + addendum
inner_r = pitch_r - dedendum
radial_depth = outer_r - inner_r
thickness = 8.0
chord = 2 * math.pi * pitch_r / num_teeth
tooth_width = chord * 0.8

# Base ring
base = cq.Workplane("XY").circle(outer_r).circle(inner_r).extrude(thickness)

# Add half the teeth
gear = base
for i in range(int(num_teeth / 2)):
    angle = i * 360.0 / num_teeth
    tooth = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .transformed(offset=(inner_r + radial_depth / 2, 0, 0))
        .rect(radial_depth, tooth_width)
        .extrude(thickness)
    )
    gear = gear.union(tooth)

# Cut away the other half of the ring and teeth
cut_box = (
    cq.Workplane("XY")
    .box(outer_r * 2, outer_r * 2, thickness + 1, centered=(True, True, True))
    .translate((0, -outer_r, thickness / 2))
)
gear = gear.cut(cut_box)

# Drill center hole
result = gear.faces(">Z").workplane(centerOption="CenterOfMass").hole(6)