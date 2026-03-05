import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Length of the plate
width = 50.0    # Width of the plate
thickness = 10.0 # Thickness of the plate

# Create the rectangular prism (box)
result = cq.Workplane("XY").box(length, width, thickness)