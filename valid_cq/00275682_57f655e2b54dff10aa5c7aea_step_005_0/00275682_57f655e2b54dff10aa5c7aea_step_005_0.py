import cadquery as cq

# Geometric parameters
width = 5.0             # Cross-section width
thickness = 5.0         # Cross-section thickness
lower_length = 50.0     # Height of the vertical bottom segment
upper_height = 50.0     # Vertical height component of the top segment
offset_x = 12.0         # Horizontal offset at the top (creates the bend angle)

# Create the path for the sweep
# The path is drawn in the Front (XZ) plane
# It starts at the origin, goes vertically up, then bends
path = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, lower_length)
    .lineTo(offset_x, lower_length + upper_height)
)

# Create the cross-section and sweep it along the path
# The profile is a rectangle created on the Bottom (XY) plane
result = (
    cq.Workplane("XY")
    .rect(width, thickness)
    .sweep(path)
)