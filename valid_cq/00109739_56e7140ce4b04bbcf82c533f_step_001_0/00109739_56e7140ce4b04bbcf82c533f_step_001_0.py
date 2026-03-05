import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the box
width = 60.0    # Width of the box
thickness = 15.0 # Thickness/Height of the box

# Create a rectangular box centered at the origin
# The box method creates a solid rectangular prism based on x, y, z dimensions
result = cq.Workplane("XY").box(length, width, thickness)