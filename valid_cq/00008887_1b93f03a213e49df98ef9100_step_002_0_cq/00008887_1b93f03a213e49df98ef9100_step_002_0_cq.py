import cadquery as cq

# Parametric dimensions
length = 1000.0  # Total length of the tube
width = 20.0     # Outer width of the square cross-section
height = 20.0    # Outer height of the square cross-section
thickness = 2.0  # Wall thickness of the tube

# Create the hollow square tube
# We start by creating a sketch for the cross-section
# 1. Create a rectangle for the outer boundary
# 2. Create a rectangle for the inner boundary
# 3. Extrude the resulting face

result = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2*thickness, height - 2*thickness)
    .extrude(length)
)