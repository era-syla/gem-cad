import cadquery as cq

# Parameters
thickness = 5
base_radius = 12.5
arm_length = 40
arm_width = 8
gap = 6
slot_depth = 2
pin_hole_diameter = 2

# Base disk
base = cq.Workplane("XY").circle(base_radius).extrude(thickness)

# Fork arms as a single bar, overlapping slightly into the base for a clean union
overlap = 1
arm = (
    cq.Workplane("XY")
    .rect(2 * arm_width + gap, arm_length + overlap)
    .extrude(thickness)
    .translate((0, base_radius - overlap / 2, 0))
)

# Combine base and arms
combined = base.union(arm)

# Central slot in the arms
slot = (
    cq.Workplane("XY")
    .box(2 * arm_width + gap, slot_depth, thickness + 1)
    .translate(
        (
            0,
            base_radius + arm_length - slot_depth / 2,
            thickness / 2,
        )
    )
)
combined = combined.cut(slot)

# Pin hole in the side of the right arm (along X axis)
pin_cut = (
    cq.Workplane("YZ", origin=(base_radius + arm_width / 2, 0, thickness / 2))
    .circle(pin_hole_diameter / 2)
    .extrude(arm_width + 1)
)
combined = combined.cut(pin_cut)

result = combined