import cadquery as cq
import math

# Screw parameters
shaft_diameter = 4.0
shaft_length = 8.0
head_diameter = 7.5
head_height = 3.0

# Create the shaft (cylinder)
shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_diameter / 2)
)

# Create thread approximation using stacked torus shapes
thread_result = shaft
pitch = 0.7
thread_depth = 0.4
num_threads = int(shaft_length / pitch)

for i in range(num_threads):
    z_pos = -shaft_length / 2 + i * pitch + pitch / 2
    thread_result = (
        thread_result
        .union(
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(shaft_diameter / 2 + thread_depth)
            .circle(shaft_diameter / 2 - 0.1)
            .extrude(pitch * 0.5)
        )
    )

# Create rounded pan head
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2)
    .circle(head_diameter / 2)
    .extrude(head_height * 0.6)
)

# Add dome top to head
dome = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height * 0.6)
    .sphere(head_diameter / 2 * 0.9)
)

# Combine head parts
head_combined = head.union(dome)

# Cut dome to proper shape - clip bottom
clip_box = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height * 0.6 + head_diameter / 2 * 0.9 + 0.1)
    .box(head_diameter * 2, head_diameter * 2, head_diameter, centered=(True, True, False))
)

head_final = head_combined.cut(
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height)
    .box(head_diameter * 2, head_diameter * 2, head_diameter, centered=(True, True, False))
)

# Merge shaft and head
screw_body = thread_result.union(head_final)

# Create Phillips head drive cutout
slot_depth = head_height * 0.8
slot_width = 1.0
slot_length = head_diameter * 0.6

# Phillips cross - two rectangular slots
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height - 0.1)
    .rect(slot_length, slot_width)
    .extrude(slot_depth, combine=False)
)

slot2 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height - 0.1)
    .rect(slot_width, slot_length)
    .extrude(slot_depth, combine=False)
)

# Phillips diagonal cuts
slot3 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height - 0.1)
    .transformed(rotate=cq.Vector(0, 0, 45))
    .rect(slot_length * 0.7, slot_width * 0.8)
    .extrude(slot_depth * 0.6, combine=False)
)

slot4 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height - 0.1)
    .transformed(rotate=cq.Vector(0, 0, -45))
    .rect(slot_length * 0.7, slot_width * 0.8)
    .extrude(slot_depth * 0.6, combine=False)
)

# Apply Phillips cutout
result = (
    screw_body
    .cut(slot1)
    .cut(slot2)
    .cut(slot3)
    .cut(slot4)
)