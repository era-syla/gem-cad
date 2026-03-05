import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Length of the plate
width = 50.0    # Width of the plate
thickness = 3.0 # Thickness of the plate

# Create the rectangular solid
# Using box() creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)