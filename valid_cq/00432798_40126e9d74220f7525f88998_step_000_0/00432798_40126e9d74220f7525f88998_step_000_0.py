import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
height = 100.0
width = 25.0
thickness = 4.0

# Create a solid rectangular prism (box)
# Based on the image orientation:
# - The longest dimension is vertical (Z-axis)
# - The wider face is visible towards the right (X-axis)
# - The narrow edge is visible towards the left (Y-axis)
result = cq.Workplane("XY").box(width, thickness, height)