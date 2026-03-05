import cadquery as cq

# Parametric dimensions for the plate
length = 100.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the solid geometry
# We start with the XY workplane and create a box (cuboid)
# centered at the origin.
result = cq.Workplane("XY").box(length, width, thickness)