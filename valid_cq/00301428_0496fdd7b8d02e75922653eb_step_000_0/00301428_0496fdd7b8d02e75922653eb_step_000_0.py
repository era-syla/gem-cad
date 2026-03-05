import cadquery as cq

# Parametric dimensions for the vertical post
height = 1000.0       # Total length of the bar
width = 40.0          # Width of the profile (x-axis)
depth = 40.0          # Depth of the profile (y-axis)
hole_diameter = 10.0  # Diameter of the hole on the top face
hole_depth = 30.0     # Depth of the top hole (blind hole)

# Create the 3D model
# 1. Create a rectangular prism (box) aligned with the Z-axis
# 2. Select the top face (+Z)
# 3. Create a centered hole on the top face
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter, hole_depth)
)