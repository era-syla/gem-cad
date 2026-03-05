import cadquery as cq

# Parametric dimensions
length = 100.0      # Length of the plate
width = 70.0        # Width of the plate
thickness = 2.0     # Thickness of the plate
fillet_radius = 6.0 # Radius of the rounded corners

# Create the model
# 1. Start with a workplane
# 2. Create a rectangular box
# 3. Select vertical edges (parallel to Z axis) to fillet corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)