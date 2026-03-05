import cadquery as cq

# Parametric Dimensions
base_r = 12.0
base_h = 10.0
shaft_r = 3.5
shaft_h = 40.0
head_core_r = 8.5
head_h = 15.0
tooth_offset = 9.0
tooth_r = 2.0
num_teeth = 12
hole_diameter = 5.0

# 1. Base, Shaft, and Head Core
result = (
    cq.Workplane("XY")
    .circle(base_r)
    .extrude(base_h)
    .faces(">Z")
    .workplane()
    .circle(shaft_r)
    .extrude(shaft_h)
    .faces(">Z")
    .workplane()
    .circle(head_core_r)
    .extrude(head_h)
)

# 2. Add Spline Teeth to Head
teeth = (
    result.faces(">Z")
    .workplane(-head_h)
    .polarArray(tooth_offset, 0, 360, num_teeth)
    .circle(tooth_r)
    .extrude(head_h)
)
result = result.union(teeth)

# 3. Add Center Through-Hole
result = result.faces(">Z").workplane().hole(hole_diameter)