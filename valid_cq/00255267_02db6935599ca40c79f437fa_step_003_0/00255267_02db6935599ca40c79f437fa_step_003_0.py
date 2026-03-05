import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 60.0    # Width of the plate
thickness = 4.0 # Thickness of the plate

# Create the rectangular plate geometry
result = cq.Workplane("XY").box(length, width, thickness)