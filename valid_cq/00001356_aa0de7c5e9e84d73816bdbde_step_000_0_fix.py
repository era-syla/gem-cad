import cadquery as cq

# Main body dimensions
length = 80
width = 60
height = 12

# Create the main body - a rounded rectangular slab
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# Apply fillets to vertical edges
result = (
    result
    .edges("|Z")
    .fillet(8)
)

# Apply chamfer/fillet to top edges
result = (
    result
    .edges(">Z")
    .fillet(3)
)

# Apply fillet to bottom edges
result = (
    result
    .edges("<Z")
    .fillet(2)
)

# Add a notch/cutout on one of the longer sides (left side based on image)
# The notch appears to be a small rectangular cutout with rounded bottom on the left side
notch_width = 12
notch_depth = 5
notch_height = 8

notch = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-length/2 - notch_depth/2, -notch_width/2, height/2 - notch_height/2))
    .box(notch_depth + 2, notch_width, notch_height)
)

# Cut the notch from the main body
result = result.cut(notch)

# Fillet the notch edges
result = (
    result
    .edges(cq.NearestToPointSelector((-length/2, 0, height/2)))
    .fillet(1.5)
)