import cadquery as cq

# Parametric dimensions based on the image aspect ratio
length = 100.0  # Horizontal dimension
width = 30.0    # Depth dimension
height = 60.0   # Vertical dimension

# Create a simple rectangular prism (box) centered at the origin
# The box method takes arguments (length, width, height) corresponding to x, y, z dimensions
result = cq.Workplane("XY").box(length, width, height)