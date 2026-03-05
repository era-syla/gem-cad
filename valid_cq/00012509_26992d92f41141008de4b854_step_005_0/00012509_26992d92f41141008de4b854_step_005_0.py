import cadquery as cq

# Parametric dimensions based on visual aspect ratio
length = 100.0  # Length of the box
width = 50.0    # Width of the box
height = 25.0   # Height of the box

# Create a simple rectangular prism (box)
# The box is centered on the origin by default
result = cq.Workplane("XY").box(length, width, height)