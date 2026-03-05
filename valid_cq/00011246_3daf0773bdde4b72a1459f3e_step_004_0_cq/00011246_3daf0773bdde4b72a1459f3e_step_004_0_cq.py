import cadquery as cq

# Define parameters for the dimensions of the rod
# Based on visual estimation, the object is a long, thin rectangular prism (square rod)
length = 100.0  # Length of the rod
width = 5.0     # Width of the square cross-section
thickness = 5.0 # Thickness of the square cross-section

# Create the 3D model
# We start with a workplane on the XY plane
# We draw a rectangle (centering it usually makes later operations easier)
# Then we extrude it to the desired length
result = (
    cq.Workplane("XY")
    .rect(width, thickness)
    .extrude(length)
)

# Alternatively, using the box primitive directly for simplicity:
# result = cq.Workplane("XY").box(width, thickness, length)