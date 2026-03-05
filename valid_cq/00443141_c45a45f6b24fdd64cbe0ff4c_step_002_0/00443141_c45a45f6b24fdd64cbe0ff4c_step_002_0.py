import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
length = 200.0   # Length of the bar
width = 10.0     # Width of the cross-section
height = 10.0    # Height of the cross-section

# Create the solid geometry
# We create a simple rectangular prism (box) using the defined dimensions.
# The box is centered at the origin by default.
result = cq.Workplane("XY").box(length, width, height)