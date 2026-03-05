import cadquery as cq

# Parameters
outer_dia = 80
body_height = 20
pocket_dia = 60
pocket_depth = 6
center_hole_dia = 8

# Build the part
result = (
    cq.Workplane("XY")
    # Base cylinder
    .circle(outer_dia / 2)
    .extrude(body_height)
    # Pocket on top
    .faces(">Z")
    .workplane()
    .circle(pocket_dia / 2)
    .cutBlind(-pocket_depth)
    # Center hole at bottom of pocket
    .workplane(offset=body_height - pocket_depth)
    .hole(center_hole_dia)
)