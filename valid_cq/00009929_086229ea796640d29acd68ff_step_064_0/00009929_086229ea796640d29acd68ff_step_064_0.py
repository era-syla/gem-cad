import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate along X-axis
width = 100.0   # Width of the plate along Y-axis
thickness = 5.0 # Thickness of the plate along Z-axis

# Create the rectangular plate centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)