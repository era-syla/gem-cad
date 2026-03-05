import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
height = 100.0  # Total height of the bar
width = 10.0    # Width of the face
thickness = 2.5 # Thickness of the profile

# Create a rectangular prism (box) centered at the origin
# The box method takes arguments for length (x), width (y), and height (z)
result = cq.Workplane("XY").box(width, thickness, height)