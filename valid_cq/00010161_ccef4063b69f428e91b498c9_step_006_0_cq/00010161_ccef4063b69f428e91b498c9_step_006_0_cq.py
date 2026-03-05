import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate
# We center the rectangle on the XY plane for convenience
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if you prefer not to center it:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(False, False, False))