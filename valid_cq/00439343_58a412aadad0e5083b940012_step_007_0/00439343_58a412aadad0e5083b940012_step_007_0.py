import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0  # Length of the plate
width = 60.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create a rectangular plate (box) centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)