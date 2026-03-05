import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 200.0  # The long dimension
width = 10.0    # The width (intermediate dimension)
thickness = 4.0 # The height/thickness (shortest dimension)

# Create a rectangular prism (box) centered at the origin
# The box method takes (length, width, height) arguments
result = cq.Workplane("XY").box(length, width, thickness)