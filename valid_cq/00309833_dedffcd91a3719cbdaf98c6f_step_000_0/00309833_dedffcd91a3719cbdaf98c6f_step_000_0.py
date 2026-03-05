import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the provided image
# The object is a rectangular prism (box) with a square profile and significant height
width = 10.0    # Width of the cross-section
depth = 10.0    # Depth of the cross-section
height = 60.0   # Total height of the prism (approx 6x the width)

# Create the CAD model
# 1. Establish a workplane on the XY plane
# 2. Sketch a centered rectangle defining the base profile
# 3. Extrude the sketch along the Z-axis to create the solid geometry
result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
)