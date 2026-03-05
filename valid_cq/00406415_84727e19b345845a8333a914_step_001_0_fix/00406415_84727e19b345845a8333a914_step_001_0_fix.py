import cadquery as cq

# Parameters
outer_length = 100
outer_width = 30
overall_height = 10
wall_thickness = 3
pocket_depth = 7
fillet_radius = 1
chamfer_distance = 0.5

# Build the frame
result = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(overall_height)
    .edges("|Z").fillet(fillet_radius)
    .edges("<Z").chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .cutBlind(-pocket_depth)
)