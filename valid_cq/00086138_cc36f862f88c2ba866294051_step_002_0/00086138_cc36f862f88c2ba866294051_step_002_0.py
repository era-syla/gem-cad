import cadquery as cq

# Parametric dimensions
length = 150.0  # The long dimension of the bar
width = 5.0     # The cross-sectional width
height = 5.0    # The cross-sectional height

# Create the rectangular prism (bar)
# The box method creates a box centered at the origin
result = cq.Workplane("XY").box(length, width, height)