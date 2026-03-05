import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the rectangular plate
width = 50.0    # Width of the rectangular plate
thickness = 1.0 # Thickness of the plate

# Create the rectangular plate geometry
result = cq.Workplane("XY").box(length, width, thickness)