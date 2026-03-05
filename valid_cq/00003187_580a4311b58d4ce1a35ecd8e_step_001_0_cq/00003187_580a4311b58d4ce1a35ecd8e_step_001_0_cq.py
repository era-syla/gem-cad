import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, using extrusion for the same result:
# result = cq.Workplane("XY").rect(length, width).extrude(thickness)