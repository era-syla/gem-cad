import cadquery as cq

# Main dimensions
length = 120
width = 80
height = 8
corner_radius = 4

# Inner recess dimensions
recess_offset = 6
recess_depth = 1.5
recess_corner_radius = 2

# Create the base box
base = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# Apply fillets to the vertical edges of the base
base = (
    base
    .edges("|Z")
    .fillet(corner_radius)
)

# Apply fillets to the top edges (horizontal)
base = (
    base
    .edges(">Z")
    .fillet(1.5)
)

# Apply small fillet to bottom edges
base = (
    base
    .edges("<Z")
    .fillet(1.0)
)

# Create the inner recess on top face
recess = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .rect(length - recess_offset * 2, width - recess_offset * 2)
    .extrude(-recess_depth)
)

# Apply fillets to recess vertical edges
recess = (
    recess
    .edges("|Z")
    .fillet(recess_corner_radius)
)

# Cut the recess from the base
result = base.cut(recess)