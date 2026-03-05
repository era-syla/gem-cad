import cadquery as cq

# Parameters
length = 100
width = 60
thickness = 5
chamfer_size = 1
pocket_length = 90
pocket_width = 50
pocket_depth = 1
top_edge_fillet = 1

# Build the plate
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    # Chamfer all vertical edges
    .edges("|Z").chamfer(chamfer_size)
    # Optional fillet around the top perimeter
    .faces(">Z").edges().fillet(top_edge_fillet)
    # Create a rectangular pocket on the top face
    .faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Expose the result
result