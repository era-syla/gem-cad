import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 80.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Generate the rectangular plate geometry
result = cq.Workplane("XY").box(length, width, thickness)