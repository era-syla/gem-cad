import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 80.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the rectangular plate
# We center it on the XY plane for convenience
result = cq.Workplane("XY").box(length, width, thickness)