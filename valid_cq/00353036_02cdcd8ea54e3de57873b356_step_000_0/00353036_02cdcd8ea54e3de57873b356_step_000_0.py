import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the bar
width = 20.0    # Width of the cross-section
height = 20.0   # Height of the cross-section

# Create the rectangular prism (box)
# The box method creates a solid centered at the origin
result = cq.Workplane("XY").box(length, width, height)