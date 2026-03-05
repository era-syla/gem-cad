import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
# The image shows a tall, slender rectangular prism (bar)
width = 10.0   # Width of the base (X axis)
depth = 10.0   # Depth of the base (Y axis)
height = 80.0  # Height of the bar (Z axis), approx 8x the width

# Create the solid geometry
# box() centers the geometry at the origin by default
result = cq.Workplane("XY").box(width, depth, height)