import cadquery as cq

# Define parametric dimensions based on the visual proportions
length = 100.0      # Length of the plate
width = 50.0        # Width of the plate
thickness = 10.0    # Thickness of the plate
fillet_radius = 10.0 # Radius of the corner fillets

# Create the 3D model
# 1. Start with a rectangular box centered on the XY plane
# 2. Select the vertical edges (parallel to Z axis)
# 3. Apply fillets to the selected edges
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)