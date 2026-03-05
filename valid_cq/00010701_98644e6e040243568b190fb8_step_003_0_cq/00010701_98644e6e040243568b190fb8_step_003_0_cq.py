import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 20.0 # Thickness of the plate

# Create the solid block
result = cq.Workplane("XY").box(length, width, thickness)