import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 50.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the simple rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)