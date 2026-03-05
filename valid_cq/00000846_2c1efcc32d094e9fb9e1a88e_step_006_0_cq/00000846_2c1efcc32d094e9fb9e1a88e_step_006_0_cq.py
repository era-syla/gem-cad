import cadquery as cq

# Define dimensions
width = 100.0   # Width of the plate
length = 100.0  # Length of the plate
thickness = 2.0 # Thickness of the plate

# Create the plate
result = cq.Workplane("XY").box(length, width, thickness)