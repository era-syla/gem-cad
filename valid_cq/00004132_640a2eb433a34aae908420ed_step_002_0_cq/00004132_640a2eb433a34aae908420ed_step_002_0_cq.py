import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the solid geometry
# We create a box centered on the XY plane for convenience
result = cq.Workplane("XY").box(length, width, thickness)