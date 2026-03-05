import cadquery as cq

# Parametric dimensions for the model
length = 100.0        # Total length of the plate
height = 40.0         # Total height of the plate
thickness = 6.0       # Thickness of the plate
corner_radius = 4.0   # Radius of the four corners of the profile
edge_radius = 1.0     # Radius of the rounded edges on the faces

# Generate the geometry
# 1. Create the base rectangular prism centered on the XY plane
# 2. Fillet the vertical edges (Z-parallel) to create the rounded corners
# 3. Fillet the remaining edges (face perimeters) to round the sharp edges
result = (
    cq.Workplane("XY")
    .box(length, height, thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .edges("#Z")
    .fillet(edge_radius)
)