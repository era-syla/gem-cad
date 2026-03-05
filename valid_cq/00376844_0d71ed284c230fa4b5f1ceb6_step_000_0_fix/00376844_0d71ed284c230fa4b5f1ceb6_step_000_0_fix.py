import cadquery as cq

# Parameters
outer_x, outer_y, thickness = 80, 50, 10
outer_fillet = 5
groove_margin = 5
groove_depth = 1
pocket_margin = 8
bottom_thickness = 3
pocket_depth = thickness - bottom_thickness

inner1_x = outer_x - 2 * groove_margin
inner1_y = outer_y - 2 * groove_margin
inner2_x = outer_x - 2 * pocket_margin
inner2_y = outer_y - 2 * pocket_margin

# Build the part
result = (
    cq.Workplane("XY")
    # Base plate
    .rect(outer_x, outer_y)
    .extrude(thickness)
    # Fillet the vertical edges
    .edges("|Z")
    .fillet(outer_fillet)
    # Switch to top face for cuts
    .faces(">Z")
    .workplane()
    # Shallow groove near the perimeter
    .rect(inner1_x, inner1_y)
    .cutBlind(groove_depth)
    # Deeper pocket inside the groove
    .rect(inner2_x, inner2_y)
    .cutBlind(pocket_depth)
)