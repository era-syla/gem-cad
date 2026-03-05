import cadquery as cq

# Define parameters for the model dimensions
length = 80.0       # Length of the plate
width = 50.0        # Width of the plate
thickness = 8.0     # Thickness of the plate
corner_radius = 8.0 # Radius for the rounded corners

# Create the 3D model
# 1. Start with a Workplane on the XY plane
# 2. Create a rectangular box centered at the origin
# 3. Select the vertical edges (parallel to the Z axis)
# 4. Apply a fillet to round the corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)