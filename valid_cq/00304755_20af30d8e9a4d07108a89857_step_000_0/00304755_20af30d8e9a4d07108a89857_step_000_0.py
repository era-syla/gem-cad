import cadquery as cq

# Parametric dimensions
length = 100.0      # Length of the plate
width = 75.0        # Width of the plate
thickness = 3.0     # Thickness of the plate
corner_radius = 5.0 # Radius for the rounded corners

# Create the model
# 1. Start with a workplane
# 2. Create a basic rectangular box
# 3. Select the vertical edges (parallel to Z axis)
# 4. Apply fillets to the selected edges
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)