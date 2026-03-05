import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
length = 100.0  # The longest dimension along the horizontal axis
height = 20.0   # The vertical dimension
thickness = 5.0 # The depth/width dimension

# Create a simple rectangular prism (box) centered at the origin
# The dimensions correspond to x (length), y (thickness), and z (height)
result = cq.Workplane("XY").box(length, thickness, height)