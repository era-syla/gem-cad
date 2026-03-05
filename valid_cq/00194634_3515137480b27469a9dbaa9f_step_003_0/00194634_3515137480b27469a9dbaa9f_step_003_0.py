import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate
width = 60.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create a rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)