import cadquery as cq

# Define parametric dimensions based on the image proportions
# The object is a rectangular prism (box)
length = 40.0  # Dimension along X axis
width = 25.0   # Dimension along Y axis
height = 100.0 # Dimension along Z axis

# Create the rectangular prism
# The box is centered at the origin by default
result = cq.Workplane("XY").box(length, width, height)