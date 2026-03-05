import cadquery as cq

# Parametric dimensions
length = 150.0   # Length of the strip
width = 20.0     # Width of the strip
thickness = 1.0  # Thickness of the strip

# Create the rectangular strip using the box operation
# By default, box centers the object at the origin
result = cq.Workplane("XY").box(length, width, thickness)