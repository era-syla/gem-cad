import cadquery as cq

# Dimensions
length = 100.0  # Length of the plate
width = 50.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the 3D model
result = cq.Workplane("XY").box(length, width, thickness)