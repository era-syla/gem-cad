import cadquery as cq

# Parameters
thickness = 3.0
width = 120.0
height = 40.0
depth = 20.0

# Build U-shaped profile in the X-Z plane and extrude in Y
profile = [
    (0, 0),
    (width, 0),
    (width, height),
    (width - thickness, height),
    (width - thickness, thickness),
    (thickness, thickness),
    (thickness, height),
    (0, height),
]
result = cq.Workplane("XZ").polyline(profile).close().extrude(depth)

# Round holes in the two vertical walls (2 columns × 3 rows)
hole_dia = 5.0
n_rows = 3
z_start = thickness + 5.0
z_end = height - 5.0
z_positions = [z_start + i * (z_end - z_start) / (n_rows - 1) for i in range(n_rows)]
x_positions = [thickness / 2, width - thickness / 2]

for x in x_positions:
    for z in z_positions:
        result = result.cut(
            cq.Workplane("XZ")
            .center(x, z)
            .circle(hole_dia / 2)
            .extrude(depth)
        )

# Two round holes in the bottom plate
bottom_hole_x = [thickness + 15.0, width - thickness - 15.0]
for x in bottom_hole_x:
    result = result.cut(
        cq.Workplane("XZ")
        .center(x, thickness / 2)
        .circle(hole_dia / 2)
        .extrude(depth)
    )

# Rectangular slot in the bottom plate
slot_width = (width - 2 * thickness) - 20.0
slot_height = thickness * 2.0
result = result.cut(
    cq.Workplane("XZ")
    .center(width / 2, thickness / 2)
    .rect(slot_width, slot_height)
    .extrude(depth)
)