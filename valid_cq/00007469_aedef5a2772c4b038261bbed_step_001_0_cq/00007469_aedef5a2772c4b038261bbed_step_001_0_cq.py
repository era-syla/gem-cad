import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Length of the plate
width = 20.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate using a simple box operation
# Centered at (0,0,0) makes it easier to position relative to other parts if needed
result = cq.Workplane("XY").box(length, width, thickness)