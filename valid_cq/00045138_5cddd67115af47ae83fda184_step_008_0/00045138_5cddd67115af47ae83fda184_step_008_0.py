import cadquery as cq

# Parametric dimensions
length = 200.0  # Length of the bar
width = 10.0    # Width of the square cross-section
height = 10.0   # Height of the square cross-section

# Create a rectangular prism (bar)
# The box method creates a solid box centered at the origin
result = cq.Workplane("XY").box(length, width, height)