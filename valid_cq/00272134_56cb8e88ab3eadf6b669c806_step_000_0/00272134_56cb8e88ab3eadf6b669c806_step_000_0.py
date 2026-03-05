import cadquery as cq

# Parametric dimensions
length = 100.0      # Total length of the bar
width = 12.0        # Width of the profile
height = 12.0       # Height of the profile
fillet_radius = 2.0 # Radius for the rounded edges

# Create the 3D model
# 1. Create a rectangular box aligned with the X-axis
# 2. Select the edges parallel to the X-axis (longitudinal edges)
# 3. Apply a fillet to round the longitudinal corners
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|X")
    .fillet(fillet_radius)
)