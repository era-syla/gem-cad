import cadquery as cq
import math

# Parameters
outer_radius = 50
inner_radius = 30
thickness = 5
slot_depth = 10
slot_width = 15
wedge_angle1 = 330
wedge_angle2 = 30
slot_angles = [180, 240]

# Base ring
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

# Wedge cutout
p1 = (0, 0)
p2 = (
    outer_radius * math.cos(math.radians(wedge_angle1)),
    outer_radius * math.sin(math.radians(wedge_angle1)),
)
p3 = (
    outer_radius * math.cos(math.radians(wedge_angle2)),
    outer_radius * math.sin(math.radians(wedge_angle2)),
)
wedge = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3])
    .close()
    .extrude(thickness)
)
result = result.cut(wedge)

# Rectangular slots
for angle in slot_angles:
    rad = inner_radius + slot_depth / 2.0
    x = rad * math.cos(math.radians(angle))
    y = rad * math.sin(math.radians(angle))
    result = (
        result
        .faces(">Z")
        .workplane()
        .transformed(offset=(x, y, 0), rotate=(0, 0, angle))
        .rect(slot_depth, slot_width)
        .cutThruAll()
    )

result