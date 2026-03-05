import cadquery as cq

# Parametric dimensions
# Top plate dimensions
plate_length = 60.0
plate_width = 30.0
plate_thickness = 2.0
corner_radius = 5.0

# Bottom block dimensions
block_length = 30.0
block_width = 15.0
block_height = 8.0

# Create the top plate with rounded corners
# We draw a rectangle, extrude it, and then fillet the vertical edges
plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the bottom block
# It needs to be attached to the bottom face of the plate
# The plate was extruded upwards from Z=0 to Z=plate_thickness, so the bottom face is at Z=0.
# We will draw on the XY plane again and extrude downwards or just create it and union.
# Let's create it relative to the global origin to keep it centered.

bottom_block = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(-block_height) # Extrude downwards
)

# Combine the parts
result = plate.union(bottom_block)

# If needed for visualization or export
# show_object(result)