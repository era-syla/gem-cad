import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate
width = 50.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate geometry
# using the box method which centers the geometry at the origin by default
result = cq.Workplane("XY").box(length, width, thickness)