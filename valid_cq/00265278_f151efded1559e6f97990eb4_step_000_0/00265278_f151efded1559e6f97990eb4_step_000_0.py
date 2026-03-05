import cadquery as cq

# Define parametric dimensions based on the visual proportions
length = 100.0   # Long horizontal dimension
height = 60.0    # Vertical dimension
thickness = 25.0 # Depth/width dimension

# Create the rectangular prism (box)
# Workplane("XY") aligns the base with the XY plane
# .box() creates a centered solid with dimensions along X, Y, and Z axes
result = cq.Workplane("XY").box(length, thickness, height)